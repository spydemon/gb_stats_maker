import re
import os

class SaveValues:
	def __init__(self, name):
		#The name of the file which contains datas.
		self.filename = name
		#Content of the new value to write in the file.
		self.newfile = []
		#Index use to know where "starts" actions. (It's complicated...)
		self.indentValue = -1

	#This function is the only one that can be call by user: it makes update of the values.
	def update(self, dico):
		#We look if the compagny is a new one.
		for element, value in dico.items():
			exists =  self.__entryAlreadyExists(element)
			if exists:
				#If the compagnie already exists, we just add the new value.
				self.__addValue(exists, value)
			else:
				#If not, we create a new entry. ;-)
				self.__addCompany(element, value)
		#We "recalibrate" indexs.
		content = self.__removeIndents()
		#We write the new data file!
		self.__writeNewFile(content)

	#For checking if the compagny already exists in the data file.	
	def __entryAlreadyExists(self, name):
		try:
			txtfile = open(self.filename, "rt")
		except IOError:
			#If the file doesn't exist, we create it and open the empty one.
			os.system("touch " + self.filename)
			txtfile = open(self.filename, "rt")
		i = 1;
		for line in txtfile:
			if line.split('=')[0] == name:
				#We return all the existing line so we just have to concatenate it with the new value.
				return line
		return 0

	#We add the new value.
	def __addValue(self, line, value):
		txtfile = open(self.filename, "rt")
		#Just a concatenation ^^
		newLine = line.replace('\n', '') + ':' + value
		self.newfile.append(newLine)

	#If we have to add a enter if the data file.
	def __addCompany(self, name, value):
		newLine = name + '='
		#Don't forget to "calibrate" index!
		newLine += self.__indent()
		self.__addValue(newLine, value)

	#For calibrating indexs	
	def __indent(self):
		if self.indentValue == -1:
			self.indentValue = self.__calculIndent()
		indent = str()
		for i in range(self.indentValue):
			#We add as wuch double points that we need for making in fact that the first value on the graph won't be at the first position, but at the position for the good day.
			indent += ':'
		return indent

	#The index is the number of entrances that we are using for the moment in the data file.
	def __calculIndent(self):
		txtfile = open(self.filename, "rt")
		numberOfEntries = txtfile.readline().count(':')
		return numberOfEntries

	#We remove lines when we sell a action because she won't appears any more on the graph. So maybe we can switch the index if the action was the older one.	
	def __removeIndents(self):
		first = True
		for line in self.newfile:
			#We have to be careful because the index is just calculate with the double points after the equal sign.
			indentInThisLine = re.search('=:*', line).group().count(':')
			if first:
				minIndent = indentInThisLine
				first = False
			if indentInThisLine < minIndent:
				minIndent = indentInThisLine
		#We realy remove the double points that we don't need anymore.
		newFileReady = []
		for entry in self.newfile:
			newFileReady.append(entry.replace(':', '', minIndent - 1))
			print "NEW VALUE : " + newFileReady[-1]
		return newFileReady

	#We write news datas on the file. Victory \o/	
	def __writeNewFile(self, content):
		txtfile = open(self.filename, "wt")
		for line in content:
			txtfile.write(line + '\n')
