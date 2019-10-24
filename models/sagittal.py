def model():
	# Les noms de reperes_anato doivent correspondrent à ceux donnés dans Kinovea
	reperes_anato = ("Hanche", "Genou", "Malleole", "Pied", "Epaule", "Coude", "Main", "Tete")

	# Le stick relie les reperes_anato pour dessiner
	stick = [3, 2, 1, 0, 4, 7, 4, 5, 6]

	# Winter
	# Definition des articulation 
	angle_seg = {
		# Articulation  # dist          # prox      # center
		"Cheville":     ("Pied",        "Genou",    "Malleole"),
		"Genou":        ("Malleole",    "Hanche",   "Genou"),
		"Hanche":       ("Genou",       "Epaule",   "Hanche"),
		"Epaule":       ("Hanche",      "Coude",    "Epaule"),
		"Coude":        ("Epaule",      "Main",     "Coude")
	}
	winter_table = {
		# Membre:   Seg_prox,    Seg_dist,   Masse,  CM_Prox, CM_Dist,  nb_seg
		"TT":       ("Epaule",   "Hanche",   0.578,  0.66,    0.34,     1),
		"Bras":     ("Epaule",   "Coude",    0.028,  0.436,   0.564,    2),
		"AvBras":   ("Coude",    "Main",     0.016,  0.43,    0.57,     2),
		"Cuisse":   ("Hanche",   "Genou",    0.1,    0.433,   0.567,    2),
		"Jambe":    ("Genou",    "Malleole", 0.0465, 0.433,   0.567,    2),
		"Pied":     ("Malleole", "Pied",     0.0145, 0.5,     0.5,      2)
	}
	
	return reperes_anato, stick, angle_seg, winter_table
