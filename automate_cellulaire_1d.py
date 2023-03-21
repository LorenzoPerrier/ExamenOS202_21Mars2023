import numpy as np
import time
import matplotlib.pyplot as plt
import sys
from mpi4py import MPI


nombre_cas: int = 256
nb_cellules: int = 360  # Cellules fantomes
nb_iterations: int = 360

compute_time = 0.
display_time = 0.

# compute propre à chaque process
single_compute_time = 0.
single_display_time = 0.

exec_time = 0.


def save_as_md(cells, symbols='⬜⬛'):
    res = np.empty(shape=cells.shape, dtype='<U')
    res[cells == 0] = symbols[0]
    res[cells == 1] = symbols[1]
    np.savetxt(f'resultat_parallele_{num_config:03d}.md', res, fmt='%s',
               delimiter='', header=f'Config #{num_config}', encoding='utf-8')


def save_as_png(cells):
    fig = plt.figure(figsize=(nb_iterations/10., nb_cellules/10.))
    ax = plt.axes()
    ax.set_axis_off()
    ax.imshow(cells[:, 1:-1], interpolation='none', cmap='RdPu')
    plt.savefig(
        f"resultat_parallele_{num_config:03d}.png", dpi=100, bbox_inches='tight')
    plt.close()


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
start = time.time()
for num_config in range(nombre_cas):
    if (rank == num_config % size):

        t1 = time.time()
        cells = np.zeros((nb_iterations, nb_cellules+2), dtype=np.int16)
        cells[0, (nb_cellules+2)//2] = 1

        for iter in range(1, nb_iterations):
            vals = np.left_shift(1, 4*cells[iter-1, 0:-2]
                                 + 2*cells[iter-1, 1:-1]
                                 + cells[iter-1, 2:])
            cells[iter, 1:-
                  1] = np.logical_and(np.bitwise_and(vals, num_config), 1)
        t2 = time.time()

        single_compute_time += t2 - t1

        t1 = time.time()
        save_as_md(cells)
        # save_as_png(cells)
        t2 = time.time()
        single_display_time += t2 - t1

# Récupération des compute / display time de chaque process. /!\ Attention il s'agit ici d'un temps cumulé car tout se fait en parallèle
compute_time = comm.reduce(single_compute_time, op=MPI.SUM, root=0)
display_time = comm.reduce(single_display_time, op=MPI.SUM, root=0)
end = time.time()
exec_time = end-start

# DISPLAY of time results
if (rank == 0):

    print(
        f"Temps total passé au calcul des generations de cellules : {compute_time:.6g}")
    print(
        f"Temps total passé à l'affichage des resultats : {display_time:.6g}")
    print(f"Total time of exécution :{exec_time:.6g}")

    # Display des graphs résultats pour la question 2
    nbp = [1, 2, 3, 4]
    tpsExec = [18.5878, 11.78, 9.56848, 8.58972]
    speedUp = [1, 18.5878/11.78, 18.5878/9.56848, 18.5878/8.58972]
    plt.subplot(211)
    plt.plot(nbp, tpsExec)
    plt.xlabel("Nombre de process")
    plt.ylabel("Temps d'exécution en seconde")
    plt.title("Temps d'exécution en fonction du nombre de process")
    plt.subplot(212)
    plt.plot(nbp, speedUp)
    plt.xlabel("Nombre de process")
    plt.ylabel("Speed Up")
    plt.title("Speed Up en fonction du nombre de process")
    plt.show()
