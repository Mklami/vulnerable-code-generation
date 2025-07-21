import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# Raw data from the table
vulnerable_data = {
    'Qwen2': [153, 66, 174, 39, 63, 41, 5, 13, 2, 1, 4],
    'Mistral': [105, 46, 62, 9, 20, 7, 2, 7, 0, 0, 3],
    'Gemma': [117, 63, 132, 32, 35, 25, 9, 14, 3, 4, 7]
}

correct_data = {
    'Qwen2': [95, 25, 80, 22, 49, 33, 3, 12, 0, 0, 4],
    'Mistral': [57, 6, 26, 5, 15, 6, 0, 3, 0, 0, 3],
    'Gemma': [72, 22, 72, 24, 29, 22, 4, 14, 0, 0, 7]
}

# Calculate Correct/Vuln percentages
correct_vuln_ratio = {}
for model in vulnerable_data.keys():
    ratios = []
    for i in range(len(vulnerable_data[model])):
        vuln = vulnerable_data[model][i]
        correct = correct_data[model][i]
        if vuln == 0:
            ratios.append(np.nan)
        else:
            ratios.append((correct / vuln) * 100)
    correct_vuln_ratio[model] = ratios

# Complexity buckets
complexity_buckets = ['[0,5)', '[5,10)', '[10,15)', '[15,20)', '[20,25)',
                     '[25,30)', '[30,35)', '[35,40)', '[40,45)', '[45,50)', '[50,100)']

# Create DataFrame for Correct/Vuln ratio
df_ratio = pd.DataFrame(correct_vuln_ratio, index=complexity_buckets)

# Create the main heatmap showing Correct/Vuln ratio with numbers and percentages
plt.figure(figsize=(10, 6))

# Create custom annotations with numbers and percentages
annotations_main = []
for i, model in enumerate(['Qwen2', 'Mistral', 'Gemma']):
    row_annotations = []
    for j, bucket in enumerate(complexity_buckets):
        vuln = vulnerable_data[model][j]
        correct = correct_data[model][j]
        ratio = correct_vuln_ratio[model][j]
        if vuln == 0 or pd.isna(ratio):
            row_annotations.append('—')
        else:
            row_annotations.append(f'{correct}/{vuln}\n{ratio:.1f}%')
    annotations_main.append(row_annotations)

annot_array_main = np.array(annotations_main)

sns.heatmap(df_ratio.T,
            annot=annot_array_main,
            fmt='',
            cmap='RdYlBu_r', # Red-Yellow-Blue reversed (red=low, blue=high)
            cbar_kws={'label': 'Correctness Rate (% of Vulnerable)', 'orientation': 'horizontal', 'shrink': 0.3, 'pad': 0.3},
            linewidths=0.5,
            square=False,
            annot_kws={'size': 14},  # Larger font for cell annotations
            vmin=0, vmax=100)

plt.xlabel('Cyclomatic Complexity Buckets', fontsize=16)
plt.ylabel('')
plt.xticks(rotation=45, ha='right', fontsize=14)
plt.yticks(rotation=90, fontsize=14) # Vertical model names

# Increase colorbar label font size
cbar = plt.gca().collections[0].colorbar
cbar.set_label('Correctness Rate (% of Vulnerable)', fontsize=16)

plt.tight_layout()
plt.subplots_adjust(bottom=0.25)  # Add space at bottom for colorbar

# Create annotated version with Vuln/Correct counts
plt.figure(figsize=(12, 6))

# Create custom annotations with Vuln/Correct counts and ratio
annotations = []
for i, model in enumerate(['Qwen2', 'Mistral', 'Gemma']):
    row_annotations = []
    for j, bucket in enumerate(complexity_buckets):
        vuln = vulnerable_data[model][j]
        correct = correct_data[model][j]
        ratio = correct_vuln_ratio[model][j]
        if vuln == 0 or pd.isna(ratio):
            row_annotations.append('—')
        else:
            row_annotations.append(f'{correct}/{vuln}\n({ratio:.1f}%)')
    annotations.append(row_annotations)

# Convert to numpy array for seaborn
annot_array = np.array(annotations)

sns.heatmap(df_ratio.T,
            annot=annot_array,
            fmt='',
            cmap='RdYlBu_r',
            cbar_kws={'label': 'Correctness Rate (% of Vulnerable)', 'orientation': 'horizontal', 'shrink': 0.3, 'pad': 0.3},
            linewidths=0.5,
            square=False,
            annot_kws={'size': 14},  # Larger font for cell annotations
            vmin=0, vmax=100)

plt.xlabel('Cyclomatic Complexity Buckets', fontsize=16)
plt.ylabel('')
plt.xticks(rotation=45, ha='right', fontsize=14)
plt.yticks(rotation=90, fontsize=14) # Vertical model names

# Increase colorbar label font size
cbar = plt.gca().collections[0].colorbar
cbar.set_label('Correctness Rate (% of Vulnerable)', fontsize=16)

plt.tight_layout()

# Create a compact version for space efficiency with numbers and percentages
plt.figure(figsize=(10, 4.2))  # Increased width to accommodate more text

# Create custom annotations for compact version
annotations_compact = []
for i, model in enumerate(['Qwen2', 'Mistral', 'Gemma']):
    row_annotations = []
    for j, bucket in enumerate(complexity_buckets):
        vuln = vulnerable_data[model][j]
        correct = correct_data[model][j]
        ratio = correct_vuln_ratio[model][j]
        if vuln == 0 or pd.isna(ratio):
            row_annotations.append('—')
        else:
            row_annotations.append(f'{correct}/{vuln}\n{ratio:.1f}%')
    annotations_compact.append(row_annotations)

annot_array_compact = np.array(annotations_compact)

sns.heatmap(df_ratio.T,
            annot=annot_array_compact,
            fmt='',
            cmap='RdYlBu_r',
            cbar_kws={'label': 'Correctness Rate (% of Vulnerable)', 'orientation': 'horizontal', 'shrink': 0.3, 'pad': 0.3},
            linewidths=0.3,
            square=False,
            annot_kws={'size': 12},  # Larger font for cell annotations
            vmin=0, vmax=100)

plt.xlabel('Cyclomatic Complexity Buckets', fontsize=14)
plt.ylabel('')
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.yticks(rotation=90, fontsize=12) # Vertical model names

# Increase colorbar label font size
cbar = plt.gca().collections[0].colorbar
cbar.set_label('Correctness Rate (% of Vulnerable)', fontsize=14)

plt.tight_layout()
plt.savefig('heatmap_correct_vuln.png', dpi=300, bbox_inches='tight')