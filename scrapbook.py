details = ['Ogrzewanie:', 'gazowe', 'Piętro:', 'parter', 'Czynsz:', 'Stan wykończenia:', 'do wykończenia', 'Rynek:', 'pierwotny', 'Forma własności:', 'Dostępne od:', 'Typ ogłoszeniodawcy:', 'prywatny', 
     'Informacje dodatkowe:', 'ogródek\ngaraż/miejsce parkingowe', 'Rok budowy:', '2024', 'Winda:', 'nie', 'Rodzaj zabudowy:', 'szeregowiec', 'Materiał budynku:', 'cegła', 'Okna:', 'plastikowe', 
     'Wyposażenie:', 'klimatyzacja', 'Zabezpieczenia:', 'rolety antywłamaniowe', 'Media:', 'internet']

# for i in range(0, len(details)):
#     print(i, details[i])

i = 0
while i < len(details):
    if ":" in details[i] and (i + 1 == len(details) or ":" in details[i + 1]):
        details.insert(i + 1, ' ')
        i += 1  # Skip the inserted element to avoid infinite loop
    i += 1

for detail in details:
    print(detail)
    if '\n' in detail:
        print(detail.replace(':', '').strip().split('\n'))
    else:
        print(detail.replace(':', '').strip())
details = [
    detail.replace(':', '').strip().split('\n') if '\n' in detail else detail.replace(':', '').strip()
    for detail in details]
print(details)            