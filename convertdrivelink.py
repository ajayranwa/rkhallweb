def create_embed_link(s):
	embed_link_temp = "https://drive.google.com/uc?export=view&id=" 
	# print(s[:32])
	if s[:32] == "https://drive.google.com/file/d/":
		res = "".join((embed_link_temp, s[32:-17]))
		# print('2')
		return res
	else:
		# print('1')
		return s

# print(create_embed_link("https://drive.google.com/file/d/1-N8ijipz1U2HICnupPasEZBO21wexDTR/view?usp=sharing"))