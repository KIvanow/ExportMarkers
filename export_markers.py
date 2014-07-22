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
		tab = '\t'

		spriteMap += "sound: { " + os.linesep + "\t resources: [ '" + str( self.view.file_name().split(os.sep)[-1:][0] ) + "', '" + str( self.view.file_name().split(os.sep)[-1:][0][ 0 : -3] ) + 'ogg' + "' ], " + os.linesep + "\tspritemap:{" + os.linesep
		spriteMap += "\t\t'empty': { " + os.linesep + "\t\t\t'start' : 0, " + os.linesep + "\t\t\t'end': 0.5, " + os.linesep + "\t\t\t'loop': false " + os.linesep + "\t\t}, " + os.linesep
		spriteMap += "\t\t'emptyLoop': { " + os.linesep + "\t\t\t'start' : 0, " + os.linesep + "\t\t\t'end': 0.5, " + os.linesep + "\t\t\t'loop': true " + os.linesep + "\t\t}, " + os.linesep

		for i in range( 0, len( words ) ):
			if 'xmpDM:frameRate' in words[ i ]:
				sampleRate = int( words[ i ].split('"')[ 1 ][ 1 : ] )

		for i in range( 0, len( words ) ):
			if 'xmpDM:name' in words[i]:
				start = int( words[i-2].split('"')[1] ) / sampleRate
				end = start + math.floor( float( words[i-1].split('"')[1] ) / sampleRate * 1000 ) / 1000
				loop = 'true' if 'loop' in words[i].split('"')[1].lower() else 'false'
				spriteMap += '\t\t"' + words[i].split('"')[1] + '": { ' + os.linesep + '\t\t\t"start": ' + str( start ) + ', ' + os.linesep + '\t\t\t"end": ' + str( end ) + ', ' + os.linesep + '\t\t\t"loop": ' + loop + os.linesep + '\t\t},' + os.linesep

		spriteMap += '\t} ' + os.linesep + '}'

		spriteFile = sublime.Window.new_file(self.view.window())
		spriteFile.insert(edit, 0, spriteMap)