import pandas as pd
import numpy as np 

categories = {
	'assists' : 'APG',
	'blocks' : 'BLKPG',
	'rebounds' : 'RPG',
	'scoring-per-game' : 'PTS',
	'steals' : 'STPG'
}
years = [2015, 2016]

def compare():
	overall = True
	for category in categories.keys():
		for year_index in range(len(years)):
			# Read and merge csv files for each category 
			filename = 'stats/' + category + '_' + str(years[year_index]) + '.csv'
			
			# Read csv to pandas data frame
			curr_df = pd.read_csv(filename)
			# Inner join on player for 2 or more data frames 
			# Join performed sequentially by year
			if year_index == 0:
				prev_df = curr_df
			elif year_index == 1:
				merge_df = pd.merge(prev_df, curr_df, on='PLAYER')
			else:
				merge_df = pd.merge(merge_df, curr_df, on='PLAYER')
		merge_df[categories[category] + '_return'] = (merge_df[categories[category] + '_y'] -  
			merge_df[categories[category] + '_x']) / merge_df[categories[category] + '_x']

		# Combine returns into one data frame across categories 
		if overall:
			overall_df =  merge_df[['PLAYER', categories[category] + '_return']]
			overall = False
		else:
			overall_df = pd.merge(overall_df, merge_df[['PLAYER', categories[category] + '_return']], on ='PLAYER')

	# Calculate total returns for players across categories, sort,  and write to csv
	overall_df = overall_df.replace([np.inf, -np.inf], np.nan)
	overall_df['Total_return'] = overall_df.sum(axis=1, numeric_only=True)
	overall_df = overall_df.sort('Total_return', ascending=False)
	overall_df.to_csv("output\output.csv")
	print overall_df

# Run main function 
if __name__ == "__main__":
	compare()