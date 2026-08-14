import pandas as pd


def recommend_funds(risk_appetite, scheme_df):

    risk_appetite = risk_appetite.strip().title()

    valid_risks = ["Low", "Moderate", "High"]

    if risk_appetite not in valid_risks:
        raise ValueError(
            "Risk appetite must be Low, Moderate, or High."
        )

    recommendations = (
        scheme_df[
            scheme_df["risk_grade"] == risk_appetite
        ]
        .dropna(subset=["sharpe_ratio"])
        .sort_values(
            "sharpe_ratio",
            ascending=False
        )
        .head(3)
        .copy()
    )

    recommendations.insert(
        0,
        "rank",
        range(1, len(recommendations) + 1)
    )

    return recommendations[
        [
            "rank",
            "amfi_code",
            "scheme_name",
            "risk_grade",
            "sharpe_ratio",
            "return_3yr_pct",
            "sortino_ratio",
            "max_drawdown_pct",
            "expense_ratio_pct"
        ]
    ]


if __name__ == "__main__":

    scheme = pd.read_csv(
        "Data/processed/07_scheme_performance.csv"
    )

    risk = input(
        "Enter risk appetite (Low / Moderate / High): "
    )

    result = recommend_funds(
        risk,
        scheme
    )

    print("\nTop 3 Fund Recommendations:\n")
    print(result.to_string(index=False))