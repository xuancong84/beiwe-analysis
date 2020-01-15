#!/usr/bin/env python3

from core import *
import datetime

def group_dates(data, labels, figsize):
    periods = [(s+'D' if s.isdigit() else s) for s in re.split('[ ,;]+', os.DateGroup)]
    index = data.index if type(data.index) == pd.DatetimeIndex else data.datetime
    max_date = index.max().floor('D')
    cut_points = [max_date]
    for period in periods[::-1]:
        max_date -= pd.to_timedelta(period)
        cut_points = [max_date] + cut_points
    dfg = data.groupby(pd.cut(index, cut_points, right=False))
    figsize[0] = len(periods)*0.4
    if index.nunique()==len(data):
        ret = dfg.mean()
        ret_index = ret.index
    else:
        ret = pd.concat([set_index_to_value(v.reset_index(drop=True), k, 'datetime') for k,v in dfg], ignore_index=True)
        ret_index = [k for k,v in dfg]
    return ret, ret_index, figsize

if __name__ == '__main__':
	# draw('moht.dsth.150@moht.com.sg_e3fb5e097f2b', None, None, 0.0, False, 'heart.csv.gz', 'grouped values by each interval', '1D', 0.0, 21,
	# 	 'time chart grouped box plot', 'HR', 'mean', '<entry-count>', False, 'no sort', False, False, False, False, True)

	# init parameters
	os.DateGroup = '30,30,7,7'
	PP = group_dates
	fig, axs = plt.subplots(nrows=1, ncols=5, figsize=[16, 4])
	Username = 'moht.dsth.150@moht.com.sg_e3fb5e097f2b'
	CyclePeriod = 21
	file_suffix = '.csv.gz'

	# sociability messages
	df = load_df(Username, 'sociabilityLog' + file_suffix).copy()
	df.orientation = df.orientation.apply(lambda t: ('outgoing' if t == 0 else 'incoming'))
	plot1a = draw(df, None, None, 0.0, False, 'sociabilityLog'+file_suffix, 'grouped values by each interval',
				'1D', 0.0, 0, 'time chart stacked bar', 'orientation', 10, '<entry-count>', True, 'no sort', True, False, False, False, None,
				post_processor=PP, ax=axs[0], set_title='WhatsApp Messages', set_ylabel='log(total#)')


