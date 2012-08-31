import os
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

class DrawGraph:
	def __init__(self, name, namePlayer, output):
		self.pName = namePlayer
		self.output = output
		#The file with values.
		self.txtfile = open(name, "rt")
		#The 2D list viths values imported.
		self.values = self.__parseValues()
		#Drawing !
		self.__printGraph()

	def __parseValues(self):
		values = []
		#In each line are stats from one compagny.
		for line in self.txtfile:
			build = []
			#We remove the \n at the end of all lines.
			splitedValues = line.replace('\n', '')
			#Because the website is frensh, fload are written with commas instead of dots. We have to make dots for matplotlib.
			splitedValues = splitedValues.replace(',', '.')
			#We split the name of the companie and his stats.
			splitedValues = splitedValues.split('=')
			#We split all stats
			build.append(splitedValues[0])
			numbers = splitedValues[1].split(':')
			#Because we've the string =: tought the name and the first stat, we have to remove the first "stat" because it's a empty value.
			del numbers[0]
			#We made all stats in a list.
			build.append(numbers)
			#And we add this list to the other list that contain the name of compagnies.
			values.append(build)
		#Don't forget to reset the virtual cursor of the file if we want to re-read it again!
		self.txtfile.seek(0)
		return values

	def __printGraph(self):
		#designLine will contain a different design for all ligns that will be draw in the graph
		symbols = ['-', '--', '-.', ':']
		colors = ['b', 'g', 'r', 'c', 'y', 'k']
		designLine = []
		for s in symbols:
			for c in colors:
				designLine.append(c + s)
		numberLine = 0

		#We start with play with plotlib.
		fig = plt.figure()
		#The second plot is use for the legend of the graph.
		ax = plt.subplot(1,2,1)

		for compagnies in self.values:
			#We need to know how many mesure we have for each compagny for knowing where in the graph the line have to begin.
			plotNumber = []
			plotValues = []
			nbreEntries = 0
			for a in compagnies[1]:
				if len(a) > 0:
					nbreEntries += 1	

			nbreValuesToCatch = nbreEntries
			topListValue = len(compagnies[1]) - 1
			#We prepare values of the graph with stats on y axis, and the number of the mesurement in the x one.
			for a in range(nbreEntries):
				nbreValuesToCatch -= 1
				plotValues.insert(0, compagnies[1][topListValue-a])
				plotNumber.insert(0, topListValue-a)
			#We draw all lines.
			ax.plot(plotNumber, plotValues, designLine[numberLine], label=compagnies[0], linewidth=1)
			numberLine += 1

		#Wearing of the graph.
		plt.title("Fluctuations des actions de " + self.pName)
		plt.xlabel("Mesures")
		plt.ylabel("Plus-value (%)")
		plt.grid(b=True, axis="y")

		#Legend's things.
		font = FontProperties()
		font.set_size('small')
		legendBox = ax.get_position()
		ax.set_position([legendBox.x0, legendBox.y0, legendBox.width * 1.5, legendBox.height])
		ax.legend(loc='center left', bbox_to_anchor=(1,0.5), prop=font)

		#Finaly: saving the graph. Mission completed!
		plt.savefig(self.output + ".png",dpi=100)
		#And moving in the good folder
		os.system("mv " + self.output + ".png graphs/")
		print "Graph available here: graphs/" + self.output + ".png\nBye!"

		#Don't forget to reset the virtual cursor of the file if we want to re-read it again!
		self.txtfile.seek(0)
