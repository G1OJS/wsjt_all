import matplotlib.pyplot as plt

def venn(ax, ns):
    x1 = n[0]/sum(ns)
    x2 = (sum(ns)-ns[2])/sum(ns)
    ax.set_axis_off()
    ax.add_patch(plt.Rectangle((0,0), x1,1, color = 'green', alpha = 0.3))
    ax.add_patch(plt.Rectangle((x1,0), x2-x1,1, color = 'yellow', alpha = 0.3))
    ax.add_patch(plt.Rectangle((x2,0),1-x2,1, color = 'red', alpha = 0.3))
    ax.text(x1/2,0.5, f'A {ns[0]}', horizontalalignment='center',verticalalignment='center')
    ax.text(x1+(x2-x1)/2,0.5, f'AB {ns[1]}', horizontalalignment='center',verticalalignment='center')
    ax.text(0.5+x2/2,0.5, f'B {ns[2]}', horizontalalignment='center',verticalalignment='center')



fig, axs = plt.subplots(3,1, figsize=(7, 9), height_ratios = (0.1,1,1))
fig.suptitle(f"Session: 1st line\n2nd line") 

n=[30,30,30]    # A, AB, B
venn(axs[0],n)
    
axs[1].set_title("Number of decodes of each callsign in session for A and B")
axs[1].set_xlabel("Number of decodes in all.txt A")
axs[1].set_ylabel("Number of decodes in all.txt B")
axs[2].set_title("SNR of all decodes in session for calls in both A and B")
axs[2].set_xlabel("SNR in all.txt A")
axs[2].set_ylabel("SNR in all.txt B")
plt.tight_layout()
plt.show()
