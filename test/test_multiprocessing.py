import time
import multiprocessing as mp

from multiprocessing.queues import Queue


def fill_queue(queue_x, queue_y):
    """ Endless process that fills the queue"""
    task = 0
    while True:
        time.sleep(0.00000001)
        queue_x.put(task)
        task += 1
        queue_y.put(task)
        # print(f"Added task {task}")
        task += 1

def queue_get_all(queue_x, queue_y):

    a = 0
    while a < 2:
        time.sleep(0.5)
        items_x = []
        items_y = []
        while not queue_x.empty() and not queue_y.empty():
            items_x.append(queue_x.get())
            items_y.append(queue_y.get())
        print(items_x)
        print(items_y)
        print(len(items_x))
        print(len(items_y))

        a += 1


if __name__ == '__main__':
    queue_x = Queue(maxsize=-1, ctx=mp.get_context())
    queue_y= Queue(maxsize=-1, ctx=mp.get_context())

    task_fill_queue = mp.Process(target=fill_queue, args=(queue_x,queue_y))
    task_fill_queue.daemon = True
    task_fill_queue.start()

    # read_queue(queue)
    queue_get_all(queue_x, queue_y)

    task_fill_queue.terminate()

    task_fill_queue.join()

