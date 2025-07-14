import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LinearSegmentedColormap
from pricing import black_scholes_price
from utils import calculate_pnl

def plot_dual_heatmap(
    spot_range,
    vol_range,
    strike,
    time,
    rate,
    purchase_price,
    quantity=1,
    vmin=-20,
    vmax=20
):
    from matplotlib.gridspec import GridSpec

    spot_vals = np.linspace(spot_range[0], spot_range[1], 20)
    vol_vals = np.linspace(vol_range[0], vol_range[1], 20)

    call_matrix = np.zeros((len(vol_vals), len(spot_vals)))
    put_matrix = np.zeros((len(vol_vals), len(spot_vals)))

    for i, vol in enumerate(vol_vals):
        for j, s in enumerate(spot_vals):
            cp = black_scholes_price(s, strike, time, rate, vol, 'call')
            pp = black_scholes_price(s, strike, time, rate, vol, 'put')
            call_matrix[i, j] = calculate_pnl(cp, purchase_price, quantity)
            put_matrix[i, j] = calculate_pnl(pp, purchase_price, quantity)

    fig = plt.figure(figsize=(18, 8), facecolor='#121212')
    gs = GridSpec(1, 3, width_ratios=[1, 1, 0.05])
    cmap = LinearSegmentedColormap.from_list("muted_rgg", ["#b22222", "#555555", "#228b22"])
    norm = Normalize(vmin=vmin, vmax=vmax)

    axes = [fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1])]
    matrices = [call_matrix, put_matrix]
    titles = ['CALL Option PnL', 'PUT Option PnL']

    for ax, mat, title in zip(axes, matrices, titles):
        im = ax.imshow(mat, cmap=cmap, norm=norm, origin='lower')
        for i in range(len(vol_vals)):
            for j in range(len(spot_vals)):
                val = mat[i, j]
                color_val = cmap(norm(val))
                brightness = 0.299 * color_val[0] + 0.587 * color_val[1] + 0.114 * color_val[2]
                text_color = 'black' if brightness > 0.6 else 'white'
                ax.text(j, i, f"{val:.0f}", ha='center', va='center', color=text_color,
                        fontsize=12, fontfamily='monospace', fontweight='bold')

        ax.set_xticks(np.arange(len(spot_vals)))
        ax.set_yticks(np.arange(len(vol_vals)))
        ax.set_xticklabels([f"{s:.0f}" for s in spot_vals], rotation=45, fontsize=12, color='white')
        ax.set_yticklabels([f"{v:.2f}" for v in vol_vals], fontsize=12, color='white')
        ax.set_xlabel("Spot Price", fontsize=14, color='white', weight='bold')
        ax.set_ylabel("Volatility", fontsize=14, color='white', weight='bold')
        ax.set_title(title, fontsize=16, color='white', weight='bold')
        ax.set_facecolor('#121212')

    # Shared colorbar
    cbar_ax = fig.add_subplot(gs[0, 2])
    cbar = fig.colorbar(im, cax=cbar_ax)
    cbar.set_label("PnL (₹)", color='white', fontsize=12, fontweight='bold')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(cbar.ax.get_yticklabels(), color='white', fontsize=11)

    fig.tight_layout()
    return fig
