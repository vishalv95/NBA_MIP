from bs4 import BeautifulSoup
from urllib2 import urlopen 
import csv

categories = {
	'assists' : 'APG',
	'blocks' : 'BLKPG',
	'rebounds' : 'RPG',
	'scoring-per-game' : 'PTS',
	'steals' : 'STPG'
}
years = [2015, 2016]

def get_tables():
	for category in categories.keys():
		for year in years:	
			# Initialize rows
			rank_count = 1

			# Create a csv file
			filename = 'stats/' + category + '_' + str(year) + '.csv'
			csvfile = open(filename, 'wb')
			writer = csv.writer(csvfile)

			for row_start in range(1,300, 40):
				rows = []
				filter_rows = []
				# Open connection to the site 
				url = 'http://espn.go.com/nba/statistics/player/_/stat/' + str(category) + '/year/' + str(year) + '/count/' + str(row_start)
				soup = BeautifulSoup(urlopen(url))

				# Get table from html
				table = soup.find('table')

				# Get and write table headers 
				if (row_start == 1):
					headers = [header.text for header in table.find('tr', attrs={"class" : "colhead"})]
					headers[0] = 'RANK' + '_' + category + '_' + str(year)
					for header in headers[2:]:
						header = header + '_' + category + '_' + str(year)
					writer.writerow(headers)

				# Get table rows
				for row in table.find_all('tr'):
					rows.append([val.text.encode('utf-8') for val in row.find_all('td')])

				# Write out rows and ranks for players
				for row in rows:
					if row[1:] != headers[1:]:
						# Write rank
						row[0] = rank_count 
						rank_count += 1

						# Remove player position
						row[1] = row[1].split(',')[0] 
						filter_rows.append(row)
				# Write to file
				writer.writerows(row for row in filter_rows)
			# Close file
			csvfile.close()

# Run main function 
if __name__ == "__main__":
	get_tables()