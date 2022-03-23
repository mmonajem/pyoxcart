import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt


file_name_seb_t = "data/seb_t.npy"
file_name_seb_factor = "data/seb_factor.npy"

def load_npy_file(filename):
    data = np.load(filename)
    return data

def huber_regression(seb_factor,seb_t):
    huber = linear_model.HuberRegressor(alpha=1E-9,epsilon=1)
    huber.fit(np.array([seb_factor]).squeeze(0).reshape(-1, 1), np.array([seb_t]).squeeze(0))
    d_seb_huber = huber.coef_.item()
    t0_seb_huber = huber.intercept_.item()          
    print('Huber -- 2 the corrected flight path lenght(slop): {:.2f}'.format(d_seb_huber), '(mm)', '\nthe corrected t_0(intercept): {:.2f}'.format(t0_seb_huber), '(ns)')
    return [d_seb_huber,t0_seb_huber]

def bayesian_ridge_regression(seb_factor,seb_t):
    bayesian_ridge = linear_model.Ridge(alpha=1)
    bayesian_ridge.fit(np.array([seb_factor]).squeeze(0).reshape(-1, 1) , np.array([seb_t]).squeeze(0))
    d_seb_rigid = bayesian_ridge.coef_.item()
    t0_seb_rigid = bayesian_ridge.intercept_.item()    
    print('ridge -- 2 the corrected flight path lenght(slop): {:.2f}'.format(d_seb_rigid), '(mm)', '\nthe corrected t_0(intercept): {:.2f}'.format(t0_seb_rigid), '(ns)')
    return [d_seb_rigid,t0_seb_rigid]

def linear_regression(seb_factor,seb_t):
    linear = linear_model.LinearRegression()
    linear.fit(np.array([seb_factor]).squeeze(0).reshape(-1, 1), np.array([seb_t]).squeeze(0))
    d_seb_linear = linear.coef_.item()
    t_seb_linear = linear.intercept_.item()
    print('Linear -- 2 the corrected flight path lenght(slop): {:.2f}'.format(d_seb_linear), '(mm)', '\nthe corrected t_0(intercept): {:.2f}'.format(t_seb_linear), '(ns)')
    return [d_seb_linear,t_seb_linear]

def lasso_regression(seb_factor,seb_t):
    lasso = linear_model.Lasso(alpha=1)
    lasso.fit(np.array([seb_factor]).squeeze(0).reshape(-1, 1), np.array([seb_t]).squeeze(0))
    d_seb_lasso = lasso.coef_.item()
    t0_seb_lasso = lasso.intercept_.item()
    print('Lasso -- 2 the corrected flight path lenght(slop): {:.2f}'.format(d_seb_lasso), '(mm)', '\nthe corrected t_0(intercept): {:.2f}'.format(t0_seb_lasso), '(ns)')
    return [d_seb_lasso,t0_seb_lasso]

def plot_regression_model(resource_dict):
    figname = "random"
    
    seb_factor = resource_dict['seb_factor']
    seb_t = resource_dict['seb_t']
    d_seb_linear = resource_dict['d_seb_linear']
    t_seb_linear = resource_dict['t_seb_linear']
    d_seb_rigid = resource_dict['d_seb_rigid']
    t0_seb_rigid = resource_dict['t0_seb_rigid']
    d_seb_huber = resource_dict['d_seb_huber']
    t0_seb_huber = resource_dict['t0_seb_huber']
    d_seb_lasso = resource_dict['d_seb_lasso']
    t0_seb_lasso = resource_dict['t0_seb_lasso']
    
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    peaks_data = plt.scatter(seb_factor, seb_t, color="black", label='peaks Ions', alpha=0.1)
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    
    linear, = plt.plot(x_vals, t_seb_linear + d_seb_linear * x_vals, '--', color='r', label='Linear' )
    rigid, = plt.plot(x_vals, t0_seb_rigid + d_seb_rigid * x_vals, '--', color='b', label='Ridge' )
    huber, = plt.plot(x_vals, t0_seb_huber + d_seb_huber * x_vals, '--', color='g', label='Huber' )
    lasso, = plt.plot(x_vals, t0_seb_lasso + d_seb_lasso * x_vals, '--', color='y', label='lasso' )
    # manual, = plt.plot(x_vals, 75 + 100 * x_vals, '--', color='y', label='manual' )
    plt.grid(color='aqua', alpha=0.3, linestyle='-.', linewidth=2)
    # plt.legend(handles=[peaks_data, linear, rigid, huber, manual], loc='lower right')
    plt.legend(handles=[peaks_data, linear, rigid, huber,lasso], loc='lower right')
    ax1.set_ylabel("Time of flight (ns)", color="red", fontsize=20)
    ax1.set_xlabel("sqrt(m/n / (k*alpha*(V_dc+beta*V_pulse)) (ns/mm)", color="red", fontsize=20)
    plt.savefig('regression' + "%s.svg" %figname, format="svg", dpi=1200)
    plt.savefig('regression' + "%s.png" %figname, format="png", dpi=1200)
    plt.show()


def main():
    resource_dict = {}
    # Get Seb_t contents
    seb_t = load_npy_file(file_name_seb_t)*1E9
    # Get Seb_factor contents
    seb_factor = load_npy_file(file_name_seb_factor)*1E6
      
    huber = huber_regression(seb_factor,seb_t)
    huber_d_seb = huber[0]
    huber_t_seb = huber[1]

    ridge = bayesian_ridge_regression(seb_factor,seb_t)
    ridge_d_seb = ridge[0]
    ridge_t_seb = ridge[1]

    linear = linear_regression(seb_factor,seb_t)
    linear_d_seb = linear[0]
    linear_t_seb = linear[1]

    lasso = lasso_regression(seb_factor,seb_t)
    lasso_d_seb = lasso[0]
    lasso_t_seb = lasso[1]

    resource_dict['seb_t'] = seb_t
    resource_dict['seb_factor'] = seb_factor
    resource_dict['d_seb_linear'] = linear_d_seb
    resource_dict['t_seb_linear'] = linear_t_seb
    resource_dict['d_seb_rigid'] = ridge_d_seb
    resource_dict['t0_seb_rigid'] = ridge_t_seb
    resource_dict['d_seb_huber'] = huber_d_seb
    resource_dict['t0_seb_huber'] = huber_t_seb
    resource_dict['d_seb_lasso'] = lasso_d_seb
    resource_dict['t0_seb_lasso'] = lasso_t_seb

    plot_regression_model(resource_dict)

    

if __name__=="__main__":
    main()