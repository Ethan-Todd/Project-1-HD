# September 1, 2026 Equity-Risk-Premium Evidence

## What is now preserved

On October 19, 2026, the official Aswath Damodaran data page and its linked monthly ERP workbook were downloaded into `source_evidence/`:

- `Damodaran_home_downloaded_2026-10-19.html` — SHA-256 `755ad4d972431c7852bc0a723630d86cbfc84b14febb259858d1938458c0e0c7`
- `Damodaran_ERPbymonth_downloaded_2026-10-19.xlsx` — SHA-256 `56605b608bad9fb49b24206954b3b38eedb364ebee0cc2663e5020e28449cc9f`

Official source URLs:

- https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm
- https://pages.stern.nyu.edu/~adamodar/pc/implprem/ERPbymonth.xlsx

## Dated observation used by the model

In the workbook's `Historical ERP` sheet, row 218 has:

| Cell | Field | September 1, 2026 value |
|---|---|---:|
| A218 | Start of month | September 1, 2026 |
| C218 | T.Bond Rate | 4.75% |
| I218 | ERP (T12 m with sustainable payout) | 4.14% |
| J218 | ERP (T12m) | 4.09% |
| Q218 | Notes | Updated growth rates |

The saved official home-page snapshot also states that the “previous month” implied ERP was 4.14% using a 4.75% U.S. Treasury rate. Because the page was current for October 1, the workbook supplies the explicit September 1 date and removes the ambiguity in “previous month.”

## Model treatment and remaining limitation

The model uses **4.14%** as the September 1, 2026 ERP observation. This source observation is now preserved and independently reproducible from the saved workbook.

This does **not** resolve the entire WACC. The model independently uses a 4.79% September 1 Treasury 10-year par yield rather than Damodaran's 4.75% workbook input. Beta, marginal debt cost, marginal tax rate, and capital-weight conventions remain estimated or provisional. Therefore, the calculated 8.1984% WACC and valuations that depend on it remain provisional even though the dated ERP observation itself is resolved.

Downloaded files are source evidence, not student-created historical records. The download date is not evidence that the files were possessed on September 1; the workbook's dated row establishes the observation that is used.
