import urllib
import re

keystat = '<td class="yfnc_tabledata1">(.+?)</td>'
date = '<th scope="col" style="border-top:2px solid #000;text-align:right; font-        weight:bold">(.+?)</th>' #obtain the date; only works for income statement
total = '<strong>(.+?)&nbsp;&nbsp;</strong>' #obtain data for any totals from statements
entry = '<td align="right">(.+?)&nbsp;&nbsp;</td>' #obtain data for any entries on     statements that are not totals


def keystatfunc(symbol):
    url = 'http://finance.yahoo.com/quote/' + symbol + '/key-statistics?p=' + symbol
    print(url)
    htmlfile = urllib.urlopen(url)
    htmltext = htmlfile.read()
    print(htmltext)
    regex = '<span id="yfs_j10_' + symbol + '">(.+?)</span>'
    pattern = re.compile(regex)
    pattern2 = re.compile(keystat)
    marketcap = re.findall(pattern, htmltext) 
    keystats = re.findall(pattern2, htmltext)
    return (marketcap + keystats[1:31]) #creates a list with all 
    #the data on key statistics page)


def statement(symbol, period, statementtype): #period: "quarter" or "annually"; statementtype: is, bs, or cf (income statement, balance sheet, cash flow statement)
    if period == "quarterly" and statementtype == "bs":
        url = 'http://finance.yahoo.com/q/bs?s=' + symbol
    elif period == "annual" and statementtype == "bs":
        url = 'http://finance.yahoo.com/q/bs?s=' + symbol + '&annual'
    elif period == "quarterly" and statementtype == "is":
        url = 'http://finance.yahoo.com/q/is?s=' + symbol + '&annual'
    elif period == "annual" and statementtype == "is":
        url = 'http://finance.yahoo.com/q/is?s=' + symbol + '&annual'
    elif period == "quarterly" and statementtype == "cf":
        url = 'http://finance.yahoo.com/q/cf?s=' + symbol + '&annual'
    elif period == "annual" and statementtype == "cf":
        url = 'http://finance.yahoo.com/q/cf?s=' + symbol + '&annual'
    htmlfile = urllib.urlopen(url)
    htmltext = htmlfile.read()
    pattern = re.compile(date)
    pattern2 = re.compile(total)
    pattern3 = re.compile(entry)
    dates = re.findall(pattern, htmltext)
    totals = re.findall(pattern2, htmltext)
    entries = re.findall(pattern3, htmltext)
    return (dates + totals + entries)



print keystatfunc("goog")

print statement("goog", "annual", "cf")