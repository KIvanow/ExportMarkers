import sublime, sublime_plugin, binascii, re, math, os
# from .bs4 import BeautifulSoup

class ExportMarkersCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		spriteMap = ''
		text = self.view.substr( sublime.Region( 0, self.view.size() ) )
		text = str( binascii.unhexlify( re.sub(re.compile(r'\s+'), '', text)) )

		text = text[ text.index('<x:xmpmeta') : text.index('</x:xmpmeta') + len( '</x:xmpmeta>' ) ].strip()
		words = text.split()

		sampleRate 	= 44100
		spritemap = ''
		newLine = '\n'
		tab = '\t'

		spriteMap = "define(function(){" + newLine + "\treturn {" + newLine
		spriteMap += "\t\tresources: [ '" + str( self.view.file_name().split(os.sep)[-1:][0] ) + "', '" + str( self.view.file_name().split(os.sep)[-1:][0][ 0 : -3] ) + 'ogg' + "' ], " + newLine + "\t\tspritemap:{" + newLine
		spriteMap += "\t\t\t'empty': { " + newLine + "\t\t\t\t'start' : 0, " + newLine + "\t\t\t\t'end': 0.5, " + newLine + "\t\t\t\t'loop': false " + newLine + "\t\t\t}, " + newLine
		spriteMap += "\t\t\t'emptyLoop': { " + newLine + "\t\t\t\t'start' : 0, " + newLine + "\t\t\t\t'end': 0.5, " + newLine + "\t\t\t\t'loop': true " + newLine + "\t\t\t}, "

		for i in range( 0, len( words ) ):
			if 'xmpDM:frameRate' in words[ i ]:
				sampleRate = int( words[ i ].split('"')[ 1 ][ 1 : ] )

		for i in range( 0, len( words ) ):
			if 'xmpDM:name' in words[i]:
				start = int( words[i-2].split('"')[1] ) / sampleRate
				end = start + math.floor( float( words[i-1].split('"')[1] ) / sampleRate * 1000 ) / 1000
				loop = 'true' if 'loop' in words[i].split('"')[1].lower() else 'false'
				spriteMap += newLine + '\t\t\t"' + words[i].split('"')[1] + '": { ' + newLine + '\t\t\t\t"start": ' + str( start ) + ', ' + newLine + '\t\t\t\t"end": ' + str( end ) + ', ' + newLine + '\t\t\t\t"loop": ' + loop + newLine + '\t\t\t},'

		spriteMap = spriteMap[ 0: -1 ] + newLine + '\t\t} ' + newLine + '\t} ' + newLine + '})'

		spriteFile = sublime.Window.new_file(self.view.window())
		spriteFile.insert(edit, 0, spriteMap)