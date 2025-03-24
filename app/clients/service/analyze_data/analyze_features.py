import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def analyze_features(csv_path, target_col="success_rate", threshold=0.1):
    # Load dataset
    df = pd.read_csv(csv_path)

    # Plot correlation heatmap for all features
    corr = df.corr()
    plt.figure(figsize=(14, 12))
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.show()

    # Select features with correlation above threshold w.r.t target
    target_corr = corr[target_col].drop(target_col)  # drop self-correlation
    recommended_features = target_corr[abs(target_corr) >= threshold].index.tolist()

    print("Recommended features (|correlation with '{}'| >= {:.2f}):".format(target_col, threshold))
    print(recommended_features)
    
    return recommended_features


if __name__ == "__main__":
    # Dynamically build relative path to your dataset
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(BASE_DIR, '../../clients/service/data_commontool_synthetic.csv')

    # Call feature analysis
    selected_features = analyze_features(csv_path)
