# Continuation Trades:

# This is a module to find continuation trade opportunities from a dataset(csv)
# In this example, we are using the Simple Moving Average (20) as our baseline
# and the Chaikin Money Flow Indicator (20) as our Confirmation Indicator

# Rules:
# Must have high data: Column A
# Must have low data: Column B
# Must have close data : Column C
# Must have volume data: Column D
# Baseline: SMA(20)
# Confirmation Indicator: CMF(20) : 0 cross

import pandas as pd

df = pd.read_csv("audnzd.csv", usecols=["high", "low", "close", "volume"])
# Input filename for inspection above

#Assign these columns to variables, convert to lists

high, low, close, volume = df["high"].tolist(), df["low"].tolist(), \
                           df["close"].tolist(), df["volume"].tolist()

# Calculate SMA(20)

sma = df["close"].rolling(window=20).mean()

# Calculate CMF(20)
# 1. Find the Money Flow Multiplier
#    [(Close  -  Low) - (High - Close)] /(High - Low) = Money Flow Multiplier

part1, part2 = (df["close"].sub(df["low"]), df["high"].sub(df["close"]))
mf1, mf2 = (part1.sub(part2), df["high"].sub(df["low"]))

mfm = mf1.div(mf2)

#mfMult = [(df["close"] - df["low"]) - (df["high"] - df["close"])] / (df["high"]
#                                                                     - df[
#                                                                     "low"])


# 2. Calculate Money Flow Volume
#    Money Flow Multiplier x Volume for the Period = Money Flow Volume

pdVol = df["volume"].rolling(window=20).mean()
mfVol = mfm.mul(pdVol)

# 3. Calculate The CMF
# 20 Period Sum of Money Flow Volume / 20 Period Sum of Volume = 20 Period CMF

sumMfVol = mfVol.rolling(window=20).sum()
sumVol = df["volume"].rolling(window=20).sum()
cmf = sumMfVol.div(sumVol)

# df.assign to add these columns

df.assign(sma=sma, cmf=cmf)





# Structure:

# Price must have never crossed the other way on your baseline
# Money management : same
# Trade even though price is past 1xATR
#
# Example:
# Baseline: 20 day SMA

# Entered Short:
# Price **crossed** and closed below SMA (Close < SMA)
# CMF is < 0
# We need a column for each parameter where 0=false, 1=true
df2 = pd.DataFrame(columns=["close<sma"])
newdf = pd.concat(df, df2)
closeSma = newdf["close<sma"]

col = 0
while col < 9:  #placeholder for loop, reflects total columns (#TODO:revise)
    if sma[0] < close[0]:
      closeSma[0]




# If CMF > 0 during trade => exit
# If the above condition occured, we look for continuation trade parameter:
#
# Price must **never** close above SMA
# We can look for the next close candle given these conditions and go from there.



