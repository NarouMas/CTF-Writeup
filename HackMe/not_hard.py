import base64

data = 'Nm@rmLsBy{Nm5u-K{iZKPgPMzS2I*lPc%_SMOjQ#O;uV{MM*?PPFhk|Hd;hVPFhq{HaAH<'
data_85 = base64.b85decode(data)
print(base64.b32decode(data_85))
