from pattern_fetching import index as pf
from future_option import index as f_o

pattern = pf()
future_option = f_o()

if not pattern.empty:
    pattern.to_csv("output/latest_output.csv", index=False)
    print("Scan completed")
else:
    # still create file so Streamlit knows scan ran
    pattern.to_csv("output/latest_output.csv", index=False)
    print("No patterns found")

if not future_option.empty:
    future_option.to_csv("output/future_output.csv", index=False)
    print("Future & Option Scan completed")
else:
    # still create file so Streamlit knows scan ran
    future_option.to_csv("output/future_output.csv", index=False)
    print("No Future & Option patterns found")
