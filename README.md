# <span style="color:#228B22">eToroPyfolio</span>, Your [<span style="color:#228B22">eToro</span>](https://www.etoro.com/) Portfolio's Data Analytics Edge

---

#### <span style="color:#B22222">Note</span>

- This is an "**unofficial**" [<span style="color:#228B22">eToro</span>](https://www.etoro.com/) portfolio data analysis package.
- This package has no relation, affiliation, or what not, with the Quantopian package, [pyfolio](https://github.com/quantopian/pyfolio).
- All variables which explicitly referring to those visible on the website are expressed between double quotation marks, " ", e.g. "Avg Open", **within this Markdown README documentation file**. On
  the other hand, **within the source code**, single quotation marks, ' ', are used instead, e.g. 'Avg Open'.
- A number of abbreviations/acronyms are used within project, such as `BRE` for `"Beginning Realized Equity"`
  <details>	
  <summary>Expand to see a more complete list of these.</summary>
  - `WD`:= `"Withdrawals"`		
  - `WDF`:= `"Withdrawal Fees"`		
  - `ROF`:= `"Roll Over Fees"`
  - `TPL`:= `"Trade Profit or Loss"`
  - `BRE`:= `"Beginning Realized Equity"`
  - `ERE`:= `"Ending Realized Equity"`
  </details>
- Any data/information unavailable in the xlsx account statement is derived/inferred. Therefore, discrepancies between the values of some variables is to be expected! 
  <details>    
  <summary>Expand to see  examples of data unavailable</summary>
  in the xlsx account statement which are approximated are:
  - "Avg Open" price of open orders. The "Avg Open" is approximated as `"Avg Open" = (Close + Open) ÷ 2` where the `Close` and `Open` values used are the open and close prices obtained
    using [yfinance](https://pypi.org/project/yfinance/) for the date the order was opened.
  - "Units" of open orders. Derived by `"Units" = "Amount" ÷ "Avg Open"`
  - "Profit" of open orders (as all "Profit" price values absent in the xlsx account statement file). Approximation via `"Profit" = ("Avg Open" - Close) x "Units"` where the `Close` price value used
    is that of the previous trading days close price.
  </details>	  
- I take **NO** no <ins>credit</ins>, nor <ins>responsibility</ins>, positive or negative, for any and all suggestion or allegement made towards or against this package.



---



## <span style="color:#228B22">eToroPyfolio</span> Developpement  Motivatrion & Reasons


### The **Egregious** & **Shamefull** [<span style="color:#228B22">eToro</span>](https://www.etoro.com/) "Account Statement" XLSX File:

"Egregious"? "Shameful"? Absolutely! Let's have a look at why this is. Pick a row in the "Closed Positions" sheet of the "Account Statement" XLSX file. Notice that the date & time format employed
by [<span style="color:#228B22">eToro</span>](https://www.etoro.com/) in both columns "Open Date" & "Close Date" is:

"%d/%m/%Y %H:%M", e.g. 16/06/2020 13:30

Now, if you have a look at the date & time format employed in the "Transactions Report" sheet,

Now, if you have a look at the date & time format employed in the "Date" column of the "Transactions Report" sheet, you'll see [<span style="color:#228B22">eToro</span>](https://www.etoro.com/)
employing the following format:

"%Y-%d-%m %H:%M:%S", e.g. 2020-06-16 13:30:05

So yeah, what is this nonsensical difference and inconsistency? Why can't the date & time formatting employed be consistent? Why must finding the transaction information associated with a certain
closed order require the additional effort of wrangling and remembering the different date & time formatting conventions employed?

Now, have a look at the date and time format employed in the "Account Details" sheet. Here, we have:

"%-m/%-d/%Y %-I:%M:%S %p", e.g. 12/20/2020 7:02:01 PM

It is, literally, as if the "Closed Positions" sheet had been filled in by
a [European](https://en.wikipedia.org/wiki/Date_and_time_notation_in_Europe#:~:text=Official%20EU%20documents%20still%20tend,YYYY%2DMM%2DDD.%22), the "Transactions Report" sheet by
a [Japanese](https://en.wikipedia.org/wiki/Date_and_time_notation_in_Japan#:~:text=The%20most%20commonly%20used%20date,%22Wednesday%2031%20December%202008%22.) and the "Account Details" sheet by
an [American](https://en.wikipedia.org/wiki/Date_and_time_notation_in_the_United_States).




#### <span style="color:#228B22">eToro</span> Date & Time Format**s**:

- Account Details (US DT Format):
    - Date Created: "%-m/%-d/%Y %-I:%M:%S %p", e.g. 12/20/2020 7:02:01 PM
    - Start Date: "%-m/%-d/%Y %-I:%M:%S %p", e.g. 1/1/2020 12:00:00 AM
    - End Date: "%-m/%-d/%Y %-I:%M:%S %p", e.g. 12/19/2020 11:59:59 PM
- Closed Positions (EU DT Format):
    - Open Date: "%d/%m/%Y %H:%M", e.g. 16/06/2020 13:30
    - Close Date: "%d/%m/%Y %H:%M", e.g. 06/07/2020 16:25
- Transactions Report (Jap DT Format):
    - Date: "%Y-%m-%d %H:%M:%S", e.g. 2020-06-16 13:30:05

#### <span style="color:#228B22">eToroPyfolio</span> Date & Time Format **Convention**:

The general guideline is to follow
the [European date & time notation](https://en.wikipedia.org/wiki/Date_and_time_notation_in_Europe#:~:text=Official%20EU%20documents%20still%20tend,YYYY%2DMM%2DDD.%22) and completely disregard
anything to do wih seconds.

- Account Details:
    - Date Created: "%d/%m/%Y %H:%M", e.g. 20/12/2020 19:02
    - Start Date: "%d/%m/%Y %H:%M", e.g. 01/01/2020 00:00
    - End Date: "%d/%m/%Y %H:%M", e.g. 19/12/2020 23:59
- Closed Positions: <- *Unchanged*
    - Open Date: "%d/%m/%Y %H:%M", e.g. 20/08/2020 14:30
    - Close Date: "%d/%m/%Y %H:%M", e.g. 14/12/2020 14:31
- Transactions Report:
    - Date: "%d/%m/%Y %H:%M", e.g. 2020-05-26 22:47

Why disregard seconds, you may be ask? Well... are you a High Frequency Trader (HFT)?

- No? Well then why does it matter?
- Yes? Mate... get out of here.



## Installation
This Python package can be installed (from PyPI) by running the following line of code in your command line:
```bash
pip install etoro-pyfolio
```





## Quick Start & Basic Usage



### Portfolio Initialisation

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam porta nisl metus, eu varius quam finibus quis. Quisque consequat enim in erat finibus ornare. Pellentesque ullamcorper odio justo, ut
rutrum tortor efficitur non.

#### Downloading Account Statement

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam porta nisl metus, eu varius quam finibus quis. Quisque consequat enim in erat finibus ornare. Pellentesque ullamcorper odio justo, ut
rutrum tortor efficitur non.

#### Portfolio Creation

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam porta nisl metus, eu varius quam finibus quis. Quisque consequat enim in erat finibus ornare. Pellentesque ullamcorper odio justo, ut
rutrum tortor efficitur non.

```python

```

# readme edit for testing branch creation w/o breaking the whole damn VCS

# read me edit for testing pulling recent changes using PyCharm after making changes on the remote on GitHub


# some random text to check naming of branches
