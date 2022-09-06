import os
import numpy as np
import matplotlib.pyplot as plt
import torch
from torch import nn
from torch.autograd import Variable
import torch.utils.data as data_utils
from torch.utils.data import Dataset

from calibration_tools import tools, data_tools
from mc import mc_tools

num_epochs = 5
batch_size = 512
batch_size_test = 4096
learning_rate = 1e-3


class CustomTensorDataset(Dataset):
    """ TensorDataset with support of transforms
    Args:
      Dataset:
    Returns:
      tensor
    """

    def __init__(self, tensors, transform=None):
        assert all(tensors[0].size(0) == tensor.size(0) for tensor in tensors)
        self.tensors = tensors
        self.transform = transform

    def __getitem__(self, index):
        x = self.tensors[0][index]

        if self.transform:
            x = self.transform(x)

        y = self.tensors[1][index]

        return x, y

    def __len__(self):
        return self.tensors[0].size(0)


class autoencoder(nn.Module):
    def __init__(self):
        super(autoencoder, self).__init__()

        self.model = nn.Sequential(
            nn.Linear(4, 128),
            nn.ReLU(True),
            nn.Linear(128, 64),
            nn.ReLU(True), nn.Linear(64, 12), nn.ReLU(True), nn.Linear(12, 1), nn.Tanh())

    def forward(self, x):
        x = self.model(x)
        return x


def normalize(data, data_original=None):
    if data_original is None:
        return (data - np.min(data)) / (np.max(data) - np.min(data))
    else:
        return (data - np.min(data_original)) / (np.max(data_original) - np.min(data_original))


def denormalize(data, data_original):
    return (data * (np.max(data_original) - np.min(data_original))) + np.min(data_original)


def test():

    dld_t = normalize(data_dld_t)
    dld_x = normalize(data_dld_x)
    dld_y = normalize(data_dld_y)
    dld_highVoltage = normalize(data_dld_highVoltage)

    data = np.concatenate([dld_t, dld_x, dld_y, dld_highVoltage], axis=1)
    model = autoencoder().cuda()
    model.load_state_dict(torch.load('./calibration.pth'))
    model.eval()

    dld_t_corr = model(data.cuda())

    dld_t_corr = dld_t_corr.cpu().data.numpy()
    dld_t_corr = denormalize(dld_t_corr, data_dld_t)

    error = dld_t_corr - data_dld_t
    plt.hist(error, bins=500)
    plt.show()
    np.save('dld_t_corr.npy', dld_t_corr)

    print('finished')

def train(model, optimizer, criterion, train_loader):
    for epoch in range(num_epochs):
        for data in train_loader:
            img = Variable(data[0]).cuda()
            target = Variable(data[1]).cuda()
            # ===================forward=====================
            output = model(img.float())
            loss = criterion(output, target.float())
            # ===================backward====================
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        # ===================log========================
        print('epoch [{}/{}], train loss:{:.8f}'
              .format(epoch + 1, num_epochs, loss.item()))

        for data in validation_loader:
            img = Variable(data[0]).cuda()
            target = Variable(data[1]).cuda()
            # ===================forward=====================
            output = model(img.float())
            loss = criterion(output, target.float())
            # ===================backward====================
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        # ===================log========================
        print('epoch [{}/{}], validation loss:{:.8f}'
              .format(epoch + 1, num_epochs, loss.item()))
        # if epoch % 10 == 0:
        #     pic = to_img(output.cpu().data)
        #     save_image(pic, './mlp_img/image_{}.png'.format(epoch))
    return model



if __name__ == '__main__':

    # dataset name
    # dataset_name = 'AL_data_b'
    dataset_name = 'OLO_AL_6_data'
    # dataset_name = 'OLO_W_6_data'
    # dataset_name = 'OLO_Ni_8_data'
    # dataset_name = 'X6Cr17_2V30Min_5_data'

    p = os.path.abspath(os.path.join("", "../../.."))

    variables_path = os.path.join(p, 'tests//results//load_crop')
    variables_result_path = os.path.join(p, 'tests/results/model/' + dataset_name)
    if not os.path.isdir(variables_result_path):
        os.makedirs(variables_result_path, mode=0o777, exist_ok=True)

    filename = variables_path + '//' + dataset_name + '//' + dataset_name + '_cropped' + '.h5'

    head, tail = os.path.split(filename)
    figname = os.path.splitext(tail)[0]

    data = data_tools.read_hdf5_through_pandas(filename)
    print(data)

    dld_highVoltage = data['dld/high_voltage'].to_numpy()
    dld_pulseVoltage = data['dld/pulse_voltage'].to_numpy()
    dld_t = data['dld/t'].to_numpy()
    dld_x = data['dld/x'].to_numpy()
    dld_y = data['dld/y'].to_numpy()

    mc_seb_ini = mc_tools.tof2mc(dld_t, 0, dld_highVoltage, dld_pulseVoltage, dld_x, dld_y, 110,
                                 mode='voltage_pulse')
    max_hist_ini, left_right_peaks_ini, peaks_sides_ini, max_paek_edges_ini, index_max_ini = tools.massSpecPlot(
        mc_seb_ini[mc_seb_ini < 100], 0.1, prominence=50, distance=100, text_loc='right', percent=50, plot=True,
        fig_name=None)
    mrp = (max_hist_ini / (left_right_peaks_ini[1] - left_right_peaks_ini[0]))
    print('Mass resolving power for the highest peak (MRP --> m/m_2-m_1):', mrp)
    for i in range(len(peaks_sides_ini)):
        print('Peaks ', i, 'is: {:.2f}'.format(peaks_sides_ini[i, 0]),
              'peak window sides are: {:.2f} - {:.2f}'.format(peaks_sides_ini[i, 2], peaks_sides_ini[i, 3]))

    max_hist_tof, left_right_peaks_tof, peaks_sides_tof, max_paek_edges_tof, index_max_tof = tools.massSpecPlot(
        dld_t[dld_t < 1000], 0.1, distance=1500, percent=50, prominence=8, plot=True, label='tof', fig_name=None)
    mrp = (max_hist_tof / (left_right_peaks_tof[1] - left_right_peaks_tof[0]))
    print('Mass resolving power for the highest peak (MRP --> m/m_2-m_1):', mrp)
    for i in range(len(peaks_sides_tof)):
        print('Peaks ', i, 'is: {:.2f}'.format(peaks_sides_tof[i, 0]),
              'peak window sides are: {:.2f} - {:.2f}'.format(peaks_sides_tof[i, 2], peaks_sides_tof[i, 3]))

    # data_dld_t = np.expand_dims(np.load('dld_t.npy'), axis=1)
    data_t = np.expand_dims(dld_x, axis=1)
    # data_t_corr = np.expand_dims(dld_t, axis=1)
    data_x = np.expand_dims(dld_x, axis=1)
    data_y = np.expand_dims(dld_y, axis=1)
    data_v_dc = np.expand_dims(dld_highVoltage, axis=1)


    t = normalize(data_t, data_dld_t)
    t_corr = normalize(data_t_corr, data_dld_t)
    x = normalize(data_x)
    y = normalize(data_y)
    v_dc = normalize(data_v_dc)

    indices = np.random.permutation(t.shape[0])
    training_idx, test_idx = indices[:int(0.8 * t.shape[0])], indices[int(0.8 * t.shape[0]):]

    t_training = np.concatenate([t[training_idx], x[training_idx], y[training_idx], v_dc[training_idx]], axis=1)
    t_test = np.concatenate([t[test_idx], x[test_idx], y[test_idx], v_dc[test_idx]], axis=1)

    t_target_training, t_target_test = t_corr[training_idx], t_corr[test_idx]

    loader = CustomTensorDataset(tensors=(torch.from_numpy(t_training), torch.from_numpy(t_target_training)),
                                 transform=None)
    train_loader = data_utils.DataLoader(loader,
                                         batch_size=batch_size, shuffle=True)

    loader_train_test = CustomTensorDataset(tensors=(torch.from_numpy(t_test), torch.from_numpy(t_target_test)),
                                            transform=None)
    validation_loader = data_utils.DataLoader(loader_train_test,
                                              batch_size=batch_size_test)

    model = autoencoder().cuda()
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, weight_decay=1e-5)

    model = train(model, optimizer, criterion, train_loader)
    model.eval()

    data = np.concatenate([t, x, y, v_dc], axis=1)
    data = torch.from_numpy(data).float()

    t_final_corr = model(data.cuda())

    t_final_corr = t_final_corr.cpu().data.numpy()
    t_final_corr = denormalize(t_final_corr, t_corr)

    error = t_final_corr - t_corr
    plt.hist(error, bins=200)
    plt.show()

    torch.save(model.state_dict(), './calibration.pth')