### The **Egregious** & **Shamefull** [<span style="color:#228B22">eToro</span>](https://www.etoro.com/) "Account Statement" XLSX File:

"Egregious"? "Shameful"? Absolutely! Let's have a look at why this is. Pick a row in the "Closed Positions" sheet of the "Account Statement" XLSX file. Notice that the date & time format employed by [<span style="color:#228B22">eToro</span>](https://www.etoro.com/) in both columns "Open Date" & "Close Date" is:

"%d/%m/%Y %H:%M", e.g. 16/06/2020 13:30

Now, if you have a look at the date & time format employed in the "Transactions Report" sheet,

Now, if you have a look at the date & time format employed in the "Date" column of the "Transactions Report" sheet, you'll see [<span style="color:#228B22">eToro</span>](https://www.etoro.com/) employing the following format:

"%Y-%d-%m %H:%M:%S", e.g. 2020-06-16 13:30:05

So yeah, what is this nonsensical difference and inconsistency? Why can't the date & time formatting employed be consistent? Why must finding the transaction information associated with a certain closed order require the additional effort of wrangling and remembering the different date & time formatting conventions employed?

Now, have a look at the date and time format employed in the "Account Details" sheet. Here, we have: 

"%-m/%-d/%Y %-I:%M:%S %p", e.g. 12/20/2020 7:02:01 PM


It is, literally, as if the "Closed Positions" sheet had been filled in by a [European](https://en.wikipedia.org/wiki/Date_and_time_notation_in_Europe#:~:text=Official%20EU%20documents%20still%20tend,YYYY%2DMM%2DDD.%22),
the "Transactions Report" sheet by a [Japanese](https://en.wikipedia.org/wiki/Date_and_time_notation_in_Japan#:~:text=The%20most%20commonly%20used%20date,%22Wednesday%2031%20December%202008%22.) and the "Account Details" sheet by an [American](https://en.wikipedia.org/wiki/Date_and_time_notation_in_the_United_States).

### <span style="color:#228B22">eToro</span> Date & Time Format**s**:

- Account Details:
    - Date Created: "%-m/%-d/%Y %-I:%M:%S %p", e.g. 12/20/2020 7:02:01 PM
    - Start Date: "%-m/%-d/%Y %-I:%M:%S %p", e.g. 1/1/2020 12:00:00 AM
    - End Date: "%-m/%-d/%Y %-I:%M:%S %p", e.g. 12/19/2020 11:59:59 PM
- Closed Positions:
    - Open Date: "%d/%m/%Y %H:%M", e.g. 16/06/2020 13:30
    - Close Date: "%d/%m/%Y %H:%M", e.g. 06/07/2020 16:25
- Transactions Report: 
  - Date: "%Y-%d-%m %H:%M:%S", e.g. 2020-06-16 13:30:05

### <span style="color:#228B22">eToroPyfolio</span> Date & Time Format **Convention**:

The general guideline is to follow the [European date & time notation](https://en.wikipedia.org/wiki/Date_and_time_notation_in_Europe#:~:text=Official%20EU%20documents%20still%20tend,YYYY%2DMM%2DDD.%22) and completely disregard anything to do wih seconds. 

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
