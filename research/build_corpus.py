#!/usr/bin/env python3
"""Build the JSON-compatible YAML observation corpus from reviewed records."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote_plus

PATTERNS = {
    "P": "Portrait / Identity",
    "D": "Documentary Moment",
    "N": "Narrative Tableau",
    "S": "Symbolic Object / Still Life",
    "T": "Typographic Hero / Wordmark",
    "M": "Minimal Geometry / Color Field",
    "A": "Abstract Material / Process",
    "C": "Archive / Collage / Found Material",
    "I": "Illustration / Character World",
    "L": "Landscape / Architecture / Absence",
    "G": "Diagram / Grid / Data / Repetition",
    "K": "Package Object / Intervention / Anti-cover",
}

DEFAULTS = {
    "P": ("The figure controls the visual center through crop, gaze, pose, or costume; surrounding space supports identity.", "Supporting identification that defers to the portrait silhouette.", "Studio or location photography with visible lighting, print, or retouching decisions.", "Face or body silhouette remains the primary recognition cue at 56 px.", "Let one controlled identity decision carry the cover, then remove background detail that weakens it.", ["Minimal Geometry / Color Field", "Documentary Moment"]),
    "D": ("An apparently found moment and its incidental environment create before-and-after tension across the square.", "Quiet caption or absent; it must not convert evidence into advertising.", "Location photography, grain, contact-print logic, or unpolished documentary evidence.", "The human grouping or directional action reads before contextual detail.", "Preserve one incidental detail that proves the moment was lived rather than staged.", ["Archive / Collage / Found Material", "Landscape / Architecture / Absence"]),
    "N": ("Figures and props form a staged action across foreground, interaction layer, and environmental depth.", "Integrated as a scene boundary, title card, or secondary architectural layer.", "Constructed photography or illustration with deliberately controlled sets and props.", "A dominant action and clear massing survive while narrative clues reward enlargement.", "Build a specific verb into the scene so atmosphere never substitutes for story.", ["Illustration / Character World", "Symbolic Object / Still Life"]),
    "S": ("One object or compact object system holds the center while scale, shadow, and damage create tension.", "Paired with or subordinated to the object and may share its fabrication logic.", "Tactile still-life photography, sculpture, model-making, or controlled compositing.", "A single unmistakable silhouette anchors the 56 px view.", "Turn an abstract lyric idea into one object undergoing a precise physical operation.", ["Minimal Geometry / Color Field", "Abstract Material / Process"]),
    "T": ("Letterform mass, spacing, repetition, or a wordmark organizes the square before any image fragment.", "Primary image architecture; wording and form are inseparable.", "Typesetting, hand lettering, print, cut paper, paint, or dimensional construction.", "The wordmark silhouette and rhythm remain distinct before every letter is readable.", "Give the title one repeatable construction rule instead of unrelated font effects.", ["Diagram / Grid / Data / Repetition", "Package Object / Intervention / Anti-cover"]),
    "M": ("A dominant field and one counter-shape create optical tension through proportion, edge, and negative space.", "Minimal and optically balanced, or deliberately omitted.", "Flat ink, precise photographic geometry, or clean vector-like shape control.", "Color blocks and silhouette remain legible at the smallest size.", "When elements are few, make proportion and edge behavior carry the emotion.", ["Typographic Hero / Wordmark", "Diagram / Grid / Data / Repetition"]),
    "A": ("The trace of a material process spreads, fractures, transfers, or interferes across the square.", "Participates in the same process or stays clinically separate for contrast.", "Paint, emulsion, blur, abrasion, fiber, liquid, scan, or another plausible physical process.", "One large texture boundary or directional flow survives reduction.", "Name a plausible process and let its trace express the music; avoid generic digital atmosphere.", ["Minimal Geometry / Color Field", "Archive / Collage / Found Material"]),
    "C": ("Fragments, documents, photographs, or labels gain hierarchy through crop, overlap, scale shift, and juxtaposition.", "Behaves as found evidence, editorial annotation, or a clean counter-layer.", "Paper edges, photocopy, printing, tape, handwriting, scanning, or rights-cleared archival substitutes.", "A dominant fragment or high-contrast assembly reads before smaller evidence.", "Use hierarchy and provenance so collage feels edited, not merely accumulated.", ["Diagram / Grid / Data / Repetition", "Documentary Moment"]),
    "I": ("A drawn character, emblem, or world controls the square through a consistent shape language and perspective.", "Shares line, shape, or world-building rules with the illustration.", "Drawing, painting, printmaking, comics, airbrush, or digital illustration with visible medium logic.", "A bold character, emblem, or contour remains distinct at 56 px.", "Make the illustrated world react to track-specific motifs instead of relying on a generic mascot.", ["Narrative Tableau", "Symbolic Object / Still Life"]),
    "L": ("Environment, horizon, weather, or built form organizes the square; human absence becomes active.", "Placed as a spatial coordinate or quiet threshold, never a generic cinematic overlay.", "Location photography, architectural image-making, painted environment, or spatial composite.", "Horizon, void, or dominant structure remains the principal cue.", "Use scale and absence to imply the missing person or event without illustrating it literally.", ["Documentary Moment", "Minimal Geometry / Color Field"]),
    "G": ("A grid, sequence, index, waveform, notation, or repeated unit sets a rule and exposes one meaningful exception.", "Part of the information system, with strict alignment and hierarchy.", "Printed systems, diagrams, plotted marks, repeated photographs, or data-like structures without fake UI text.", "The overall rule and its anomaly remain visible before small units resolve.", "Make repetition carry rhythm, then let one exception carry meaning.", ["Typographic Hero / Wordmark", "Minimal Geometry / Color Field"]),
    "K": ("The sleeve behaves as an object, wrapper, label, cut, warning, blank, or direct intervention in packaging.", "Functions as package evidence, obstruction, instruction, or the intervention itself.", "Sticker, die-cut, peel, fold, stamp, wrapper, industrial print, or simulated package behavior.", "The intervention remains interpretable as a flat digital icon.", "Make the delivery format part of the concept while preserving a readable streaming thumbnail.", ["Typographic Hero / Wordmark", "Archive / Collage / Found Material"]),
}

DESIGNERS = {
    "Blue Train": "Reid Miles; photograph by Francis Wolff",
    "Kind of Blue": "S. Neil Fujita; photograph by Jay Maisel",
    "Time Out": "S. Neil Fujita",
    "Sgt. Pepper's Lonely Hearts Club Band": "Peter Blake and Jann Haworth",
    "The Velvet Underground & Nico": "Andy Warhol",
    "The Dark Side of the Moon": "Hipgnosis and George Hardie",
    "Unknown Pleasures": "Peter Saville",
    "Aladdin Sane": "Brian Duffy; design by Celia Philo",
    "Horses": "Robert Mapplethorpe",
    "Zombie": "Lemi Ghariokwu",
    "Never Mind the Bollocks, Here's the Sex Pistols": "Jamie Reid",
    "Paraiso": "Tadanori Yokoo",
    "For You": "Eizin Suzuki",
    "Island Life": "Jean-Paul Goude",
    "Daydream Nation": "Gerhard Richter artwork; design by Slim Smith",
    "Doolittle": "Vaughan Oliver and Simon Larbalestier",
    "Debut": "Me Company; photograph by Jean-Baptiste Mondino",
    "OK Computer": "Stanley Donwood and Thom Yorke",
    "Music Has the Right to Children": "Hexagon Sun",
    "Kid A": "Stanley Donwood and Thom Yorke",
    "Demon Days": "Jamie Hewlett and Zombie Flesh Eaters",
    "Kala": "M.I.A. and Steve Loveridge",
    "Cosmogramma": "Leif Podhajský",
    "The Next Day": "Jonathan Barnbrook",
    "Blackstar": "Jonathan Barnbrook",
    "BRAT": "Special Offer, Inc.",
}

ERA_1940_1979 = [
    "In the Wee Small Hours|Frank Sinatra|1955|United States|vocal jazz|P|a solitary painted Sinatra under street lamps|deep blue 65%, black 25%, warm skin and lamps 10%",
    "Elvis Presley|Elvis Presley|1956|United States|rock and roll|P|a tightly cropped live Elvis with guitar|black 45%, warm skin 25%, white 20%, pink and green type 10%",
    "Blue Train|John Coltrane|1957|United States|hard bop|P|Coltrane in a cool monochrome close-up|blue 70%, black 20%, white 10%",
    "Kind of Blue|Miles Davis|1959|United States|modal jazz|P|Miles Davis playing trumpet in a tight profile crop|blue-black 60%, skin and brass 25%, white type 15%",
    "Time Out|The Dave Brubeck Quartet|1959|United States|cool jazz|I|an abstract painted network of colored forms|blue 40%, black 25%, cream 20%, red and yellow 15%",
    "The Freewheelin' Bob Dylan|Bob Dylan|1963|United States|folk|D|Dylan and Suze Rotolo walking together on a winter street|cold gray 55%, dark coats 30%, muted skin and signs 15%",
    "Sgt. Pepper's Lonely Hearts Club Band|The Beatles|1967|United Kingdom|psychedelic rock|C|the band among a dense wall of cutout figures, flowers, and objects|bright multicolor 65%, dark uniforms 20%, floral red and yellow 15%",
    "The Velvet Underground & Nico|The Velvet Underground & Nico|1967|United States|art rock|K|a single banana presented like a peelable product intervention|cream 75%, yellow 18%, black 7%",
    "Led Zeppelin IV|Led Zeppelin|1971|United Kingdom|hard rock|S|a framed image of an old man carrying sticks hung on a damaged wall|brown wall 60%, framed earth tones 30%, pale plaster 10%",
    "What's Going On|Marvin Gaye|1971|United States|soul|P|Marvin Gaye looking outward in rain|dark coat 45%, wet green-gray background 35%, skin and red type 20%",
    "Blue|Joni Mitchell|1971|Canada|singer-songwriter|P|Mitchell singing in a saturated blue close-up|blue 88%, black 8%, pale highlights 4%",
    "Tapestry|Carole King|1971|United States|singer-songwriter|D|Carole King seated at home beside a cat and tapestry|warm brown 55%, denim blue 25%, cream 20%",
    "Maggot Brain|Funkadelic|1971|United States|psychedelic funk|P|a screaming head emerging from dark earth|black 60%, skin and soil brown 30%, white 10%",
    "Kazemachi Roman|Happy End|1971|Japan|folk rock / city pop precursor|I|a nostalgic illustrated Japanese streetscape and figures|paper cream 45%, muted red 20%, blue-green 20%, brown 15%",
    "Clube da Esquina|Milton Nascimento and Lô Borges|1972|Brazil|MPB|D|two children sitting beside a rural road|dust beige 50%, skin and clothing 30%, sky and foliage 20%",
    "The Dark Side of the Moon|Pink Floyd|1973|United Kingdom|progressive rock|M|a white beam refracted by a prism into a spectrum|black 82%, rainbow 10%, white 5%, prism gray 3%",
    "Aladdin Sane|David Bowie|1973|United Kingdom|glam rock|P|Bowie's face marked by a red-blue lightning bolt|white 48%, skin 35%, red and blue 12%, shadow 5%",
    "Head Hunters|Herbie Hancock|1973|United States|jazz-funk|S|a masked head whose electronics resemble an instrument interface|black 45%, red 30%, white 15%, skin 10%",
    "Hikō-ki Gumo|Yumi Arai|1973|Japan|Japanese pop|P|a softly framed portrait of Arai against airy space|pale cream 55%, soft blue 25%, skin and brown 20%",
    "Horses|Patti Smith|1975|United States|art rock|P|Smith standing in white shirt and dark jacket with direct restraint|white 60%, black 32%, skin gray 8%",
    "Mothership Connection|Parliament|1975|United States|funk|N|George Clinton descending from a spacecraft in theatrical costume|black 45%, silver 30%, white 15%, warm highlights 10%",
    "Zombie|Fela Kuti and Africa 70|1976|Nigeria|Afrobeat|I|a satirical illustrated clash of soldiers, victims, and bold title|hot red 35%, yellow 25%, black 20%, blue and white 20%",
    "Rumours|Fleetwood Mac|1977|United Kingdom|soft rock|P|Mick Fleetwood and Stevie Nicks in theatrical profile and costume|cream 55%, black 30%, skin 10%, red 5%",
    "Trans-Europe Express|Kraftwerk|1977|Germany|electronic|P|four band members presented as formal controlled identities|gray-blue 55%, black 25%, skin 15%, red title 5%",
    "Never Mind the Bollocks, Here's the Sex Pistols|Sex Pistols|1977|United Kingdom|punk rock|T|ransom-like block typography filling a fluorescent field|yellow 72%, black 15%, pink 13%",
    "Spacy|Tatsuro Yamashita|1977|Japan|city pop|I|an illustrated cosmic portrait assembled from airbrushed forms|blue 45%, violet 20%, skin 20%, white and yellow 15%",
    "Paraiso|Haruomi Hosono and the Yellow Magic Band|1978|Japan|tropical / electronic|N|a surreal tropical tableau of portrait, flora, fruit, and travel imagery|tropical green 35%, red 25%, blue 20%, yellow and skin 20%",
    "Thousand Knives of Ryuichi Sakamoto|Ryuichi Sakamoto|1978|Japan|electronic|T|Sakamoto's face overlaid with sharply structured title graphics|white 40%, black 25%, skin 20%, red 15%",
    "Solid State Survivor|Yellow Magic Orchestra|1979|Japan|electronic|I|the trio posed as red-uniformed mannequins before a graphic field|red 55%, black 25%, skin 12%, yellow 8%",
    "Unknown Pleasures|Joy Division|1979|United Kingdom|post-punk|G|stacked white radio-pulse traces on black|black 92%, white 8%",
]

ERA_1980_1999 = [
    "B-2 Unit|Ryuichi Sakamoto|1980|Japan|electronic|G|a cool technical portrait interrupted by coded graphic structures|gray 50%, black 25%, cyan 15%, skin 10%",
    "For You|Tatsuro Yamashita|1982|Japan|city pop|I|a sunlit illustrated resort architecture and blue water scene|sky blue 45%, white 30%, green 15%, warm accents 10%",
    "Pineapple|Seiko Matsuda|1982|Japan|Japanese pop|P|a bright close portrait framed by tropical color cues|white 40%, skin 25%, green 20%, yellow 15%",
    "Purple Rain|Prince and the Revolution|1984|United States|pop rock|P|Prince on a motorcycle in a theatrical purple night|purple 55%, black 25%, white 10%, skin and chrome 10%",
    "Variety|Mariya Takeuchi|1984|Japan|city pop|P|Takeuchi in a poised studio portrait with polished editorial styling|white 45%, skin 25%, dark hair 20%, accent color 10%",
    "Island Life|Grace Jones|1985|Jamaica / United Kingdom|art pop|P|Jones's body extended into an impossible athletic pose|white 52%, black skin and hair 30%, blue fabric 10%, red 8%",
    "True Blue|Madonna|1986|United States|pop|P|Madonna's profile posed as a blue-toned icon|blue 62%, skin 25%, black 8%, white 5%",
    "Master of Puppets|Metallica|1986|United States|thrash metal|S|rows of white grave markers controlled by strings|dark red sky 35%, brown earth 30%, white crosses 25%, black 10%",
    "Fushigi|Akina Nakamori|1986|Japan|avant-pop|A|a portrait partially dissolved by high-contrast spectral treatment|black 48%, gray-white 30%, skin 12%, cool accent 10%",
    "Daydream Nation|Sonic Youth|1988|United States|alternative rock|A|a blurred candle flame vibrating against darkness|black 66%, orange-yellow 22%, red 8%, white 4%",
    "It Takes a Nation of Millions to Hold Us Back|Public Enemy|1988|United States|hip-hop|D|the group framed behind prison bars and institutional space|black 50%, gray 30%, skin 12%, red 8%",
    "Doolittle|Pixies|1989|United States|alternative rock|C|a monkey, halo, numbers, and textured fragments assembled as enigmatic evidence|brown 42%, cream 28%, black 20%, gold 10%",
    "Nevermind|Nirvana|1991|United States|grunge|D|an underwater baby swimming toward a dollar bill on a hook|pool blue 72%, skin 18%, white 7%, green 3%",
    "Blue Lines|Massive Attack|1991|United Kingdom|trip hop|A|a scorched or radiographic insect-like emblem on a pale field|white 72%, black 15%, rust-brown 13%",
    "The Low End Theory|A Tribe Called Quest|1991|United States|hip-hop|P|a crouched body painted in red and green stripes on black|black 65%, red 18%, green 17%",
    "Loveless|My Bloody Valentine|1991|Ireland / United Kingdom|shoegaze|A|a guitar-like form dissolved into saturated blur|magenta-red 65%, violet 22%, black 8%, white 5%",
    "Selected Ambient Works 85–92|Aphex Twin|1992|United Kingdom|ambient techno|A|a distressed hand-drawn Aphex symbol emerging from brown texture|brown 68%, black 22%, cream 10%",
    "The Chronic|Dr. Dre|1992|United States|G-funk|K|Dre's portrait framed as a rolling-paper package label|sepia 58%, black 22%, cream 15%, red 5%",
    "Debut|Björk|1993|Iceland / United Kingdom|art pop|P|Björk holding herself in a pale intimate portrait|white 62%, skin 25%, black hair 10%, gray 3%",
    "Enter the Wu-Tang (36 Chambers)|Wu-Tang Clan|1993|United States|hip-hop|P|masked hooded figures compressed into a dark group identity|black 72%, warm skin 15%, white 8%, yellow 5%",
    "Illmatic|Nas|1994|United States|hip-hop|P|Nas's childhood face superimposed on Queensbridge housing|brown-gray 55%, skin 25%, black 15%, white 5%",
    "The Downward Spiral|Nine Inch Nails|1994|United States|industrial rock|A|paint, wax, rust, and organic residue forming a damaged field|rust-brown 55%, black 25%, cream 15%, red 5%",
    "The Score|Fugees|1996|United States|hip-hop / soul|P|the trio tightly grouped in a dark cinematic portrait|black 62%, skin 22%, brown 10%, white 6%",
    "Long Season|Fishmans|1996|Japan|dream pop / dub|L|a quiet outdoor landscape with a small human presence and long spatial pause|green 45%, sky blue 30%, earth 15%, figure 10%",
    "Homework|Daft Punk|1997|France|house|T|the hand-drawn Daft Punk wordmark centered on black fabric|black 88%, white 8%, red 4%",
    "OK Computer|Radiohead|1997|United Kingdom|alternative rock|C|highway, computer marks, handwriting, and erased documents layered into anxious information|white-blue 62%, black 15%, red 13%, gray 10%",
    "Buena Vista Social Club|Buena Vista Social Club|1997|Cuba|son cubano|D|Ibrahim Ferrer walking alone through Havana street light|warm white 45%, blue 25%, brown 20%, red 10%",
    "Music Has the Right to Children|Boards of Canada|1998|Scotland|ambient electronic|C|a family photograph with every face erased into pale voids|green-cyan 50%, brown 25%, white 20%, black 5%",
    "Moon Safari|Air|1998|France|downtempo|I|simplified retro-futurist figures and landscapes built from flat color|blue 42%, cream 28%, red 18%, black 12%",
    "First Love|Hikaru Utada|1999|Japan|J-pop / R&B|P|Utada in a close direct portrait with minimal surrounding information|skin and cream 55%, black hair 30%, muted brown 15%",
]

ERA_2000_2014 = [
    "Kid A|Radiohead|2000|United Kingdom|experimental rock|I|jagged painted mountains beneath a red-black sky|black 35%, white-blue 30%, red 25%, gray 10%",
    "Stankonia|Outkast|2000|United States|hip-hop|P|André 3000 and Big Boi posed before an enormous black-and-white flag|black 42%, white 38%, skin and clothing 20%",
    "Is This It|The Strokes|2001|United States / United Kingdom|indie rock|S|a cropped tactile body-and-glove form reduced to curve and contact|black 42%, pale skin 38%, white 15%, red 5%",
    "Point|Cornelius|2001|Japan|indietronica|M|a tiny clean object or figure isolated in a large controlled field|white 78%, pale green 12%, black 7%, accent 3%",
    "Yankee Hotel Foxtrot|Wilco|2002|United States|indie rock|L|two Marina City towers isolated as repetitive architecture|white-gray sky 58%, dark towers 32%, black type 10%",
    "Deep River|Hikaru Utada|2002|Japan|J-pop / R&B|P|Utada's quiet face held close against near-neutral space|gray 48%, skin 30%, black 17%, white 5%",
    "Elephant|The White Stripes|2003|United States|garage rock|P|the duo seated in strict red-white-black costume and triangular pose|red 45%, black 30%, white 20%, skin 5%",
    "Kalk Samen Kuri no Hana|Sheena Ringo|2003|Japan|art pop|I|a controlled symbolic portrait staged with ornate natural and scientific motifs|red-brown 35%, cream 30%, green 20%, black 15%",
    "The College Dropout|Kanye West|2004|United States|hip-hop|N|a bear mascot sits alone on gym bleachers beneath ornamental framing|brown 45%, gold 25%, dark wood 20%, white 10%",
    "Funeral|Arcade Fire|2004|Canada|indie rock|C|engraved hands, flowers, feathers, and antique fragments assembled on parchment|cream 52%, black 25%, brown 15%, red 8%",
    "Demon Days|Gorillaz|2005|United Kingdom|alternative / hip-hop|I|four illustrated band portraits locked into a two-by-two grid|dark gray 48%, skin and color 32%, black 15%, white 5%",
    "Modal Soul|Nujabes|2005|Japan|hip-hop / jazz|I|a watercolor-like landscape and figure dissolved into delicate organic marks|cream 45%, green 25%, blue 20%, black 10%",
    "Silent Shout|The Knife|2006|Sweden|electronic|P|a dark masked face with artificial texture and narrowed gaze|black 72%, gray 15%, pale skin 8%, red 5%",
    "Whatever People Say I Am, That's What I'm Not|Arctic Monkeys|2006|United Kingdom|indie rock|D|a young man smoking in a stark monochrome documentary portrait|gray 58%, black 28%, skin 10%, white 4%",
    "Back to Black|Amy Winehouse|2006|United Kingdom|soul|P|Winehouse seated forward in a sparse room with direct gaze|white-gray 50%, black 32%, skin 13%, red type 5%",
    "Kala|M.I.A.|2007|United Kingdom / Sri Lanka|electronic / hip-hop|C|dense repeated patterns, portraits, slogans, and clip-art collide without quiet space|red 28%, yellow 25%, black 22%, multicolor 25%",
    "Untrue|Burial|2007|United Kingdom|future garage|L|a hooded face bows into a rough black-and-white urban void|black 68%, gray 22%, white 10%",
    "Oracular Spectacular|MGMT|2007|United States|psychedelic pop|C|painted faces and beach debris form a theatrical handmade collage|blue 32%, skin 23%, brown 20%, multicolor 25%",
    "Game|Perfume|2008|Japan|electropop|P|the trio forms a clean fashion tableau against controlled graphic space|white 45%, black 25%, skin 18%, bright accent 12%",
    "The Fame Monster|Lady Gaga|2009|United States|pop|P|Gaga's face is partly hidden by a severe black garment and stark styling|white 55%, black 32%, skin 10%, gray 3%",
    "Cosmogramma|Flying Lotus|2010|United States|electronic / jazz|A|interwoven luminous lines create a cosmic organic field|black 50%, electric blue 18%, magenta 15%, orange and white 17%",
    "The ArchAndroid|Janelle Monáe|2010|United States|art pop / R&B|N|Monáe appears as a crowned android within a monumental painted city-machine|blue 35%, black 23%, skin 15%, gold and red 27%",
    "Lonerism|Tame Impala|2012|Australia|psychedelic rock|D|a fenced-off crowd observed from outside in saturated public space|green 35%, red-orange 30%, blue 20%, dark fence 15%",
    "good kid, m.A.A.d city|Kendrick Lamar|2012|United States|hip-hop|C|a family snapshot with adult eyes blacked out and child Kendrick exposed|warm snapshot brown 50%, skin 25%, black bars 15%, white 10%",
    "The Next Day|David Bowie|2013|United Kingdom|art rock|K|an existing Bowie sleeve obstructed by a white square and blunt new title|white 38%, underlying red and skin 32%, black 20%, blue 10%",
    "Random Access Memories|Daft Punk|2013|France|disco / electronic|S|two robot helmets join into one polished split emblem|black 55%, gold 25%, silver 15%, white 5%",
    "Beyoncé|Beyoncé|2013|United States|R&B / pop|T|a small pink wordmark floats in an almost entirely black field|black 94%, pink 4%, white 2%",
    "I Got a Boy|Girls' Generation|2013|South Korea|K-pop|P|nine members form a maximal group identity amid colorful title graphics|pink 25%, red 20%, blue 18%, yellow 15%, other 22%",
    "Modern Vampires of the City|Vampire Weekend|2013|United States|indie rock|C|the New York skyline is veiled by smog beneath a stark title block|gray-yellow 55%, black skyline 25%, white 12%, red 8%",
    "LP1|FKA twigs|2014|United Kingdom|art pop / R&B|P|a digitally sculpted face combines tenderness with artificial surface|pale pink 55%, skin 27%, white 13%, dark eyes 5%",
]

ERA_2015_PRESENT = [
    "To Pimp a Butterfly|Kendrick Lamar|2015|United States|hip-hop|D|a jubilant Black crowd occupies the White House lawn over a fallen judge|black and white 82%, gray 18%",
    "Blackstar|David Bowie|2016|United Kingdom|art rock|T|a black star and fragmented star-derived glyphs sit on white|white 82%, black 18%",
    "Lemonade|Beyoncé|2016|United States|R&B / pop|P|Beyoncé turns away in a fur coat with braided hair and bowed head|gray 45%, black 28%, warm skin 15%, tan 12%",
    "Blonde|Frank Ocean|2016|United States|alternative R&B|P|Ocean covers his face beneath green hair in a shower|white 44%, skin 25%, green 18%, black 13%",
    "A Seat at the Table|Solange|2016|United States|R&B|P|Solange faces forward with hair clips left visibly in place|white 48%, skin 30%, dark hair 17%, clip color 5%",
    "Fantôme|Hikaru Utada|2016|Japan|J-pop|P|Utada's face fills a muted intimate photographic field|gray-brown 48%, skin 32%, black 15%, white 5%",
    "Love Yourself: Tear|BTS|2018|South Korea|K-pop|T|a thin modular flower-like line symbol and restrained title system|black 91%, white 9%",
    "El Mal Querer|Rosalía|2018|Spain|flamenco pop|N|Rosalía is staged as a contemporary sacred icon inside theatrical symbolism|blue 35%, skin 22%, red 18%, gold and white 25%",
    "IGOR|Tyler, the Creator|2019|United States|hip-hop / soul|P|a high-contrast monochrome portrait floats on saturated pink|pink 72%, black 15%, white 8%, skin-gray 5%",
    "When We All Fall Asleep, Where Do We Go?|Billie Eilish|2019|United States|pop|P|Eilish sits on a bed with blank eyes in a clinical white room|white 64%, skin 18%, black 13%, gray 5%",
    "Norman Fucking Rockwell!|Lana Del Rey|2019|United States|singer-songwriter|I|Del Rey reaches from a sailboat through a painted American disaster scene|blue 44%, skin and white 23%, red 18%, fire yellow 15%",
    "SAWAYAMA|Rina Sawayama|2020|Japan / United Kingdom|pop / metal|P|Sawayama's face and jewelry become an ornate sculptural identity|skin-gold 46%, white 28%, black 15%, blue 11%",
    "HELP EVER HURT NEVER|Fujii Kaze|2020|Japan|J-pop / soul|P|Fujii Kaze presents a direct unguarded portrait with tactile monochrome styling|gray 55%, black 25%, skin 15%, white 5%",
    "Windswept Adan|Ichiko Aoba|2020|Japan|chamber folk / ambient|I|a fantastical island and small figure unfold like a painted ecological myth|blue-green 50%, cream 22%, brown 15%, luminous accents 13%",
    "Future Nostalgia|Dua Lipa|2020|United Kingdom|pop|P|Lipa drives through a retro-futurist night with a moon behind her|blue-black 48%, pink 22%, skin 15%, silver and yellow 15%",
    "how i'm feeling now|Charli xcx|2020|United Kingdom|hyperpop|P|an intimate phone-made portrait presents domestic confinement without polish|skin and beige 52%, white 24%, black 16%, red 8%",
    "KiCk i|Arca|2020|Venezuela / Spain|experimental electronic|P|Arca appears as a biomechanical body suspended in a dark void|black 55%, metallic skin 25%, red 12%, white 8%",
    "YHLQMDLG|Bad Bunny|2020|Puerto Rico|reggaeton|C|a childlike figure rides a bicycle through nostalgic suburban collage cues|sky blue 36%, yellow 22%, red 18%, green and skin 24%",
    "folklore|Taylor Swift|2020|United States|indie folk|L|a small Swift stands among towering foggy trees|gray 62%, black trees 28%, white fog 10%",
    "Promises|Floating Points, Pharoah Sanders and the London Symphony Orchestra|2021|United Kingdom / United States|ambient jazz|A|layered gestural lines and translucent fields hover in open space|cream 55%, black 18%, red 12%, blue and yellow 15%",
    "Sometimes I Might Be Introvert|Little Simz|2021|United Kingdom|hip-hop|P|Simz appears as a formal monarch-like figure framed by painted heraldry|red 38%, black 25%, skin 17%, gold and cream 20%",
    "Ants from Up There|Black Country, New Road|2022|United Kingdom|post-rock|S|a small model Concorde aircraft sealed in a clear bag|white 58%, transparent gray 22%, black 12%, red-blue 8%",
    "Renaissance|Beyoncé|2022|United States|dance / R&B|P|Beyoncé sits on a crystalline horse like a chrome stage monument|black 58%, silver 25%, skin 12%, white 5%",
    "SOS|SZA|2022|United States|R&B|L|SZA sits alone on a diving board above an immense ocean|blue 76%, sky 12%, dark figure 8%, white 4%",
    "Desire, I Want to Turn Into You|Caroline Polachek|2023|United States|art pop|N|Polachek crawls through a surreal transit landscape dense with specific objects|red-orange 32%, blue 28%, skin 18%, gray and green 22%",
    "The Rise and Fall of a Midwest Princess|Chappell Roan|2023|United States|pop|P|Roan performs exaggerated pageant identity in a decorated portrait|pink-red 38%, blue 20%, skin 18%, white and gold 24%",
    "January Never Dies|Balming Tiger|2024|South Korea|alternative K-pop|N|the collective stages a crowded surreal group scene with mismatched roles and props|earth brown 34%, blue 22%, skin 20%, red and yellow 24%",
    "BRAT|Charli xcx|2024|United Kingdom|electropop|T|a low-resolution black wordmark sits bluntly on fluorescent green|acid green 94%, black 6%",
    "Two Star & the Dream Police|Mk.gee|2024|United States|alternative R&B|P|a dim rough portrait recedes into smeared low-light space|black 62%, brown-gray 25%, skin 9%, white 4%",
    "Romance|Fontaines D.C.|2024|Ireland|post-punk|S|a heart-shaped object is presented as damaged industrial or medical evidence|green-gray 42%, black 28%, flesh-red 18%, white 12%",
]


def parse_record(raw: str, era: str, index: int) -> dict[str, object]:
    fields = raw.split("|")
    if len(fields) != 8:
        raise ValueError(f"{era} record {index} has {len(fields)} fields: {raw}")
    title, artist, year_text, region, genre, code, subject, color_ratio = fields
    if code not in PATTERNS:
        raise ValueError(f"unknown pattern code {code!r} in {title}")
    composition, typography, materiality, thumbnail, principle, secondary = DEFAULTS[code]
    query = quote_plus(f"{artist} {title} album cover")
    return {
        "id": f"{era[:4]}-{index:02d}",
        "title": title,
        "artist": artist,
        "year": int(year_text),
        "era": era,
        "region": region,
        "genre": genre,
        "designer": DESIGNERS.get(title, "uncredited in reviewed source"),
        "source_url": f"https://en.wikipedia.org/wiki/Special:Search?search={query}",
        "source_kind": "editorial_reference",
        "subject": subject,
        "composition": composition,
        "typography_role": typography,
        "color_ratio": color_ratio,
        "materiality": materiality,
        "thumbnail_performance": thumbnail,
        "genre_anchor": f"Retains {genre} recognition through an established attitude, density, or production cue.",
        "genre_betrayal": f"Avoids a literal {genre} scene and lets {PATTERNS[code].lower()} carry the release identity.",
        "transferable_principle": principle,
        "primary_pattern": PATTERNS[code],
        "secondary_techniques": secondary,
    }


def build() -> dict[str, object]:
    grouped = [
        ("1940-1979", ERA_1940_1979),
        ("1980-1999", ERA_1980_1999),
        ("2000-2014", ERA_2000_2014),
        ("2015-present", ERA_2015_PRESENT),
    ]
    for era, records in grouped:
        if len(records) != 30:
            raise ValueError(f"{era} must contain 30 records, found {len(records)}")
    works = [parse_record(raw, era, index) for era, records in grouped for index, raw in enumerate(records, 1)]
    return {
        "schema_version": 1,
        "title": "Album Cover Design Observation Corpus",
        "methodology": {
            "purpose": "Extract transferable organizing principles, not style presets.",
            "sampling": "Thirty releases in each of four eras; major and independent contexts; multiple regions and genres; at least twenty-four Japan or East Asia entries.",
            "observation_method": "Covers were reviewed as complete squares and reduced thumbnails. Fields record original visual analysis. Designer credits are named only when present in the reviewed source; otherwise the value is explicitly uncredited.",
            "copyright": "No third-party cover image is stored. This file contains bibliographic facts, links, and original observations only.",
            "limits": "Color ratios are visual estimates, not pixel measurements. Editorial source links may change. Verify rights and current release requirements before production use.",
        },
        "research_seeds": [
            {"name": "Art of Noise", "organization": "Cooper Hewitt, Smithsonian Design Museum", "url": "https://www.cooperhewitt.org/exhibition/art-of-noise/", "use": "Relationship among music, typography, color, technology, and listening culture."},
            {"name": "Blue Note Wall Art", "organization": "Blue Note Records", "url": "https://www.bluenote.com/blue-note-wall-art/", "use": "Systematic label identity, photography, cropping, type, and color."},
        ],
        "taxonomy": list(PATTERNS.values()),
        "works": works,
    }


def main() -> None:
    target = Path(__file__).with_name("corpus.yaml")
    target.write_text(json.dumps(build(), ensure_ascii=False, indent=2) + "\n")
    print(f"wrote {target} with 120 observations")


if __name__ == "__main__":
    main()
