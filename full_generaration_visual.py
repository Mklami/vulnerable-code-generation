import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def create_compact_horizontal_plot():
    """
    Create a compact horizontal plot with grouped layout
    """
    
    # Data extracted from Tables I and II - reorganized by strategy
    data = {
        'Model_Strategy': [
            'Qwen2', 'Mistral', 'Gemma',  # Dynamic group
            'Qwen2', 'Mistral', 'Gemma'   # Reverse group
        ],
        'Strategy_Group': [
            'Dynamic', 'Dynamic', 'Dynamic',
            'Reverse', 'Reverse', 'Reverse'
        ],
        'Total_Prompts': [2040, 2040, 2040, 1250, 1250, 1250],
        'Compilable': [1912, 1079, 1711, 917, 407, 690],
        'Vulnerable_Total': [1069, 715, 1207, 561, 261, 441],
        'Correct_Vulnerability': [800, 387, 718, 323, 141, 266]
    }
    
    results = []
    for i in range(len(data['Model_Strategy'])):
        total = data['Total_Prompts'][i]
        compilable = data['Compilable'][i]
        vulnerable = data['Vulnerable_Total'][i]
        correct = data['Correct_Vulnerability'][i]
        
        non_compilable = total - compilable
        no_vulnerability = compilable - vulnerable
        wrong_vulnerability = vulnerable - correct
        correct_vulnerability = correct
        
        results.append({
            'Model_Strategy': data['Model_Strategy'][i],
            'Strategy_Group': data['Strategy_Group'][i],
            'Non_Compilable_Pct': (non_compilable / total) * 100,
            'No_Vulnerability_Pct': (no_vulnerability / total) * 100,
            'Wrong_Vulnerability_Pct': (wrong_vulnerability / total) * 100,
            'Correct_Vulnerability_Pct': (correct_vulnerability / total) * 100,
            'Total': total
        })
    
    df = pd.DataFrame(results)
    
    # Create compact plot with grouped layout
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    
    colors = ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4']
    y_positions = [0, 1, 2, 3.2, 4.2, 5.2]  # Smaller gap between groups
    height = 0.7
    
    # Stack the horizontal bars
    left1 = np.zeros(len(df))
    left2 = df['Non_Compilable_Pct']
    left3 = df['Non_Compilable_Pct'] + df['No_Vulnerability_Pct']
    left4 = df['Non_Compilable_Pct'] + df['No_Vulnerability_Pct'] + df['Wrong_Vulnerability_Pct']
    
    ax.barh(y_positions, df['Non_Compilable_Pct'], height, left=left1, 
            label='Non-Compilable', color=colors[0], alpha=0.8)
    ax.barh(y_positions, df['No_Vulnerability_Pct'], height, left=left2, 
            label='No Vulnerability', color=colors[1], alpha=0.8)
    ax.barh(y_positions, df['Wrong_Vulnerability_Pct'], height, left=left3,
            label='Wrong Vulnerability', color=colors[2], alpha=0.8)
    ax.barh(y_positions, df['Correct_Vulnerability_Pct'], height, left=left4,
            label='Correct Vulnerability', color=colors[3], alpha=0.8)
    
    # Add percentage labels for all categories
    for i, (idx, row) in enumerate(df.iterrows()):
        y_pos = y_positions[i]
        # Non-compilable
        if row['Non_Compilable_Pct'] > 4:  # Only show if >= 4%
            ax.text(row['Non_Compilable_Pct']/2, y_pos, f"{row['Non_Compilable_Pct']:.1f}%", 
                   ha='center', va='center', fontweight='bold', color='white', fontsize=9)
        
        # No vulnerability
        x_pos = row['Non_Compilable_Pct'] + row['No_Vulnerability_Pct']/2
        ax.text(x_pos, y_pos, f"{row['No_Vulnerability_Pct']:.1f}%", 
               ha='center', va='center', fontweight='bold', color='white', fontsize=9)
        
        # Wrong vulnerability
        if row['Wrong_Vulnerability_Pct'] > 4:  # Only show if >= 4%
            x_pos = row['Non_Compilable_Pct'] + row['No_Vulnerability_Pct'] + row['Wrong_Vulnerability_Pct']/2
            ax.text(x_pos, y_pos, f"{row['Wrong_Vulnerability_Pct']:.1f}%", 
                   ha='center', va='center', fontweight='bold', color='white', fontsize=9)
        
        # Correct vulnerability
        x_pos = (row['Non_Compilable_Pct'] + row['No_Vulnerability_Pct'] + 
                row['Wrong_Vulnerability_Pct'] + row['Correct_Vulnerability_Pct']/2)
        ax.text(x_pos, y_pos, f"{row['Correct_Vulnerability_Pct']:.1f}%", 
               ha='center', va='center', fontweight='bold', color='white', fontsize=9)
    
    # Add group labels between the groups, positioned better
    # Add horizontal lines and labels to separate groups
    ax.axhline(y=2.6, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    
    # Add vertical group labels outside the plot area
    ax.text(103, 1, 'Dynamic', ha='center', va='center', fontsize=11, fontweight='bold', 
            rotation=90, bbox=dict(boxstyle="round,pad=0.2", facecolor='lightblue', alpha=0.7))
    ax.text(103, 4.2, 'Reverse', ha='center', va='center', fontsize=11, fontweight='bold', 
            rotation=90, bbox=dict(boxstyle="round,pad=0.2", facecolor='lightcoral', alpha=0.7))
    
    ax.set_ylabel('Strategy', fontsize=10, fontweight='bold')
    ax.set_xlabel('Percentage (%)', fontsize=10, fontweight='bold')
    ax.set_yticks(y_positions)
    ax.set_yticklabels(df['Model_Strategy'], fontsize=9)
    
    # Create custom legend at the bottom of the plot
    legend_elements = [
        plt.Rectangle((0, 0), 1, 1, facecolor=colors[0], alpha=0.8, label='Non-Compilable'),
        plt.Rectangle((0, 0), 1, 1, facecolor=colors[1], alpha=0.8, label='No Vulnerability'),
        plt.Rectangle((0, 0), 1, 1, facecolor=colors[2], alpha=0.8, label='Wrong Vulnerability'),
        plt.Rectangle((0, 0), 1, 1, facecolor=colors[3], alpha=0.8, label='Correct Vulnerability')
    ]
    
    # Position legend at the bottom center of the plot
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.1), 
              ncol=4, frameon=False, fontsize=9)
    
    ax.grid(axis='x', alpha=0.3)
    # Fixed: Set xlim to start at 0 so bars start at y-axis
    ax.set_xlim(0, 105)  # Changed from (-8, 100) to (0, 105)
    ax.invert_yaxis()
    
    plt.tight_layout()
    plt.subplots_adjust(left=0.08)  # Reduce left margin to minimize gap
    return fig, df

# Test the function
if __name__ == "__main__":
    print("Creating compact horizontal plot...")
    fig, df = create_compact_horizontal_plot()
    plt.show()