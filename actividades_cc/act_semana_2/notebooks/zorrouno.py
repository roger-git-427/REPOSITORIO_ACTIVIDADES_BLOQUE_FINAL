import pandas as pd
class Processor:
    @staticmethod
    def embbed(d):
        d.columns = d.columns.str.strip()  # Clean column names

        try:
            d = d[['Net Income to Total Assets', 'ROA(A) before interest and % after tax',
                   'ROA(B) before interest and depreciation after tax',
                   'ROA(C) before interest and depreciation before interest',
                   'Net worth/Assets', 'Debt ratio %',
                   'Persistent EPS in the Last Four Seasons',
                   'Retained Earnings to Total Assets',
                   'Net profit before tax/Paid-in capital',
                   'Per Share Net profit before tax (Yuan ¥)',
                   'Current Liability to Assets', 'Working Capital to Total Assets',
                   "Net Income to Stockholder's Equity", 'Borrowing dependency',
                   'Current Liability to Current Assets', 'Liability to Equity',
                   'Net Value Per Share (A)', 'Net Value Per Share (B)',
                   'Net Value Per Share (C)', 'Current Liability to Equity',
                   'Bankrupt?']]
        except KeyError as e:
            print('Missing columns:', e)
            return None
        return d
