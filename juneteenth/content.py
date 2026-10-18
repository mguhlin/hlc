# -*- coding: utf-8 -*-
"""English content for the Juneteenth & the Meaning of Freedom collection.

The English text of each string is also its translation key (see build.py).
Historical statements are paraphrased from the linked primary and secondary
sources; the full General Order No. 3 text is quoted from the U.S. National
Archives. Generated illustrations are not used as historical evidence.
"""

UI = {
    'collection': 'Juneteenth & the Meaning of Freedom',
    'footer_credit': '© 2026 TCEA · CC BY-NC 4.0 content · MIT code · Built with AI assistance, human-reviewed.',
    'land_lede': (
        'Primary-source investigations, timelines, and celebrations that trace June 19, 1865, '
        'from Galveston to a federal holiday. Students read General Order No. 3, weigh what '
        'freedom meant in practice, and connect the past to how Texans mark the day today.'),
    'land_teks_body': (
        'Activities align to the TEKS in force now. The State Board of Education completed its '
        'K–12 social studies revision in September 2026; districts begin implementing the new '
        'standards in 2030–31 for the early grades, with high-school courses following in 2033–34. '
        'Each activity carries a blank 2026 TEKS field to complete once crosswalks are published.'),
    'land_source_note': (
        'Primary source for this collection: NEA, “Teaching Juneteenth and the Meaning of Freedom.” '
        'Historical statements link to original records; generated illustrations are not historical evidence.'),
}

# Shared hard-history guidance -------------------------------------------------
HH_K2 = ('Keep the focus on freedom and celebration. If children ask, answer simply and truthfully: '
         'long ago some people were held in slavery and were not free, and Juneteenth celebrates the day '
         'word came that they were free. Follow children’s questions and feelings, and use the book and '
         'images your community has approved. (Guidance: Teaching for Change.)')
HH_35 = ('Use precise language — enslaved people, not “slaves,” and enslavers — and keep the focus on the '
         'freedom people claimed. Teach emancipation as part of U.S. history, and help students separate '
         'what a source actually shows from what they infer. (Framework: Learning for Justice, Teaching Hard History.)')
HH_612 = ('Teach slavery and emancipation as central to U.S. history, not a side note. Use precise language '
          '— enslaved people, enslavers — and keep people, not systems alone, at the center. Center the agency '
          'of the freed, and examine the gap between freedom as law and freedom in practice. '
          '(Framework: Learning for Justice, Teaching Hard History.)')

# Reusable source links --------------------------------------------------------
NARA_GO3 = {'text': 'National Archives · General Order No. 3',
            'url': 'https://www.archives.gov/news/articles/juneteenth-and-general-order-no-3'}
NARA_13 = {'text': 'National Archives · 13th Amendment',
           'url': 'https://www.archives.gov/milestone-documents/13th-amendment'}
NARA_EP = {'text': 'National Archives · Emancipation Proclamation',
           'url': 'https://www.archives.gov/milestone-documents/emancipation-proclamation'}
UNT_LESSON = {'text': 'Texas History for Teachers · Texas Today lesson (UNT)',
              'url': 'https://education.texashistory.unt.edu/downloads/documents/7/units/civil-war/lessons/texas-today/all/lesson-plan-and-teacher-guide.docx'}
UNT_WS = {'text': 'Texas Today worksheet, Advanced (UNT)',
          'url': 'https://education.texashistory.unt.edu/downloads/documents/7/units/civil-war/lessons/texas-today/all/worksheet-advanced.docx'}
PBS = {'text': 'PBS NewsHour Classroom · History of Juneteenth',
       'url': 'https://www.pbs.org/newshour/classroom/2022/06/lesson-plan-history-of-juneteenth-and-why-its-set-to-become-a-national-holiday/'}
DOCSTEACH = {'text': 'DocsTeach · Juneteenth General Order lesson',
             'url': 'https://projectreconstructionus.com/items/show/33'}
PORTAL = {'text': 'The Portal to Texas History (UNT)', 'url': 'https://texashistory.unt.edu'}
CNN_FLAG = {'text': 'CNN · What the Juneteenth flag means',
            'url': 'https://www.cnn.com/2022/06/17/us/juneteenth-flag-meaning-explainer-cec'}
NMAAHC = {'text': 'NMAAHC Kids · Juneteenth resource',
          'url': 'https://nmaahc.si.edu/sites/default/files/files/nmaahc_kids_-_juneteenth_resource.pdf'}
MAZIE = {'text': 'Read-aloud · Juneteenth for Mazie', 'url': 'https://www.youtube.com/watch?v=CPTGD1D9pCI'}
OPAL = {'text': 'Interview · Opal Lee', 'url': 'https://www.youtube.com/watch?v=UhJol9z0ICQ'}

# Full General Order No. 3 text (National Archives) ----------------------------
GO3_TEXT = ('“The people of Texas are informed that, in accordance with a proclamation from the Executive of '
            'the United States, all slaves are free. This involves an absolute equality of personal rights and '
            'rights of property between former masters and slaves, and the connection heretofore existing between '
            'them becomes that between employer and hired labor. The freedmen are advised to remain quietly at '
            'their present homes and work for wages. They are informed that they will not be allowed to collect '
            'at military posts and that they will not be supported in idleness either there or elsewhere.”')
GO3_CITE = ('General Order No. 3, Headquarters District of Texas, Galveston, June 19, 1865, issued by '
            'Major General Gordon Granger. U.S. National Archives.')


CONTENT = [
    # ====================== K–2 ======================
    {
        'slug': 'celebration-sort', 'band': 'K–2', 'format': 'Sort the traditions',
        'title': 'Celebration Sort',
        'card': 'Sort holiday traditions into Juneteenth, Independence Day, or both.',
        'intro': ('Some traditions belong to Juneteenth. Some belong to Independence Day. Some belong to both. '
                  'Pick each card and put it where it fits.'),
        'can': 'name a tradition and tell which holiday it belongs to.',
        'objective': ('Students identify customs associated with national holidays and distinguish Juneteenth '
                      'from Independence Day.'),
        'response': 'Draw one way your family or community celebrates. Tell a friend which holiday it belongs to.',
        'hard_history': HH_K2,
        'teks': {'code': 'K.1(B), 1.1(B)',
                 'se': 'Identify customs associated with national patriotic holidays; compare observances past and present.'},
        'engine': {
            'type': 'sort',
            'buckets': [{'id': 'jun', 'text': 'Juneteenth'},
                        {'id': 'ind', 'text': 'Independence Day'},
                        {'id': 'both', 'text': 'Both holidays'}],
            'items': [
                {'text': 'Drinking red soda or strawberry drinks', 'cat': 'jun'},
                {'text': 'Hearing General Order No. 3 read aloud', 'cat': 'jun'},
                {'text': 'Fireworks on the Fourth of July', 'cat': 'ind'},
                {'text': 'Hearing the Declaration of Independence', 'cat': 'ind'},
                {'text': 'A family cookout and a parade', 'cat': 'both'},
                {'text': 'Celebrating freedom in the United States', 'cat': 'both'},
            ],
        },
        'source': {
            'cite': ('Juneteenth marks June 19, 1865, when U.S. Army troops brought word to Galveston, Texas, '
                     'that enslaved people were free.'),
            'links': [NMAAHC],
        },
        'answer_key': [
            'Juneteenth: red soda or strawberry drinks; hearing General Order No. 3 read aloud.',
            'Independence Day: Fourth of July fireworks; hearing the Declaration of Independence.',
            'Both holidays: a family cookout and a parade; celebrating freedom in the United States.',
        ],
        'discussion': [
            'What is your family’s favorite way to celebrate a holiday?',
            'Both holidays celebrate freedom. How are they different?',
            'Why do people read an important paper out loud on a holiday?',
        ],
    },
    {
        'slug': 'story-path', 'band': 'K–2', 'format': 'Put the story in order',
        'title': 'Story Path',
        'card': 'After the read-aloud, put the Juneteenth story moments in order.',
        'intro': ('Listen to the read-aloud of a Juneteenth story. Then put the moments in the order they happened, '
                  'first to last.'),
        'can': 'retell a story in the order it happened.',
        'objective': 'Students describe the origin of a holiday and sequence events after a read-aloud.',
        'response': 'Draw your favorite part. Tell what happened just before it and just after it.',
        'hard_history': HH_K2,
        'teks': {'code': '1.1(A)', 'se': 'Describe the origins of customs, holidays, and celebrations.'},
        'engine': {
            'type': 'sequence',
            'items': [
                {'text': 'Long ago, some people were enslaved and were not free.', 'order': 0, 'shuffle': 2},
                {'text': 'President Lincoln signed a paper saying enslaved people would be free.', 'order': 1, 'shuffle': 0},
                {'text': 'Soldiers came to Galveston, Texas, and shared the news: everyone was free.', 'order': 2, 'shuffle': 4},
                {'text': 'Families celebrated with food, music, and prayer.', 'order': 3, 'shuffle': 1},
                {'text': 'Today we remember that day every June 19.', 'order': 4, 'shuffle': 3},
            ],
        },
        'source': {
            'cite': 'Based on the historical sequence behind Juneteenth. Pair with a read-aloud such as Juneteenth for Mazie.',
            'links': [MAZIE, NMAAHC],
        },
        'answer_key': [
            'Order: people were enslaved → Lincoln’s proclamation → the news reaches Galveston → families celebrate → we remember every June 19.',
        ],
        'discussion': [
            'How do you think people felt when they heard the news?',
            'Why do we remember this day every year?',
            'What part of the story would you want to ask more about?',
        ],
    },
    {
        'slug': 'flag-decoder', 'band': 'K–2', 'format': 'Tap to reveal',
        'title': 'Flag Decoder',
        'card': 'Tap each part of the Juneteenth flag to learn what it stands for.',
        'intro': 'The Juneteenth flag is full of meaning. Tap each part to learn what it stands for.',
        'can': 'explain what a symbol on the flag stands for.',
        'objective': 'Students interpret the symbols of the Juneteenth flag.',
        'response': 'Draw the Juneteenth flag. Label one part and tell what it means.',
        'hard_history': HH_K2,
        'teks': {'code': '1.1(A); Grade 2 culture strand',
                 'se': 'Explain the meaning of symbols; identify ethnic and cultural celebrations.',
                 'verify': True},
        'engine': {
            'type': 'reveal',
            'parts': [
                {'text': 'The star', 'detail': ('The star stands for Texas, where the last enslaved people in the '
                                                'Confederacy learned they were free. It also stands for freedom in all 50 states.')},
                {'text': 'The burst around the star', 'detail': ('The burst, like a new star in the sky (a nova), '
                                                                 'stands for a new beginning and a new freedom.')},
                {'text': 'The arc (the curved line)', 'detail': 'The arc is a new horizon — the hopes and chances ahead for free people.'},
                {'text': 'Red, white, and blue', 'detail': ('These are the colors of the U.S. flag. They show that enslaved '
                                                            'people and their descendants were, and are, Americans.')},
                {'text': 'The date June 19, 1865', 'detail': ('Many flags add this date — the day freedom was announced '
                                                             'in Galveston, Texas.')},
            ],
        },
        'source': {
            'cite': 'The Juneteenth flag was designed in 1997 by Ben Haith and illustrated by Lisa Jeanne Graf.',
            'links': [CNN_FLAG],
        },
        'answer_key': [
            'Star: Texas and freedom for all 50 states.',
            'Burst: a new beginning and new freedom.',
            'Arc: a new horizon of hope and opportunity.',
            'Red, white, and blue: enslaved people and their descendants were, and are, Americans.',
            'June 19, 1865: the day freedom was announced in Galveston.',
        ],
        'discussion': [
            'Which part of the flag is your favorite? Why?',
            'Why do you think the flag uses the same colors as the U.S. flag?',
            'If you made a flag for freedom, what would you put on it?',
        ],
    },
    # ====================== 3–5 ======================
    {
        'slug': 'freedom-timeline', 'band': '3–5', 'format': 'Order the timeline',
        'title': 'Freedom Timeline',
        'card': 'Put key dates in order, from Galveston in 1865 to the federal holiday.',
        'intro': 'Put these moments in order, from the earliest to the most recent.',
        'can': 'place events in the correct order and explain what changed.',
        'objective': 'Students sequence the events of emancipation and describe the impact of the Civil War and Reconstruction on Texas.',
        'response': 'Choose two events next to each other. Explain what changed from the first to the second.',
        'hard_history': HH_35,
        'teks': {'code': '4.4(A)', 'se': 'Describe the impact of the Civil War and Reconstruction on Texas.'},
        'engine': {
            'type': 'sequence',
            'items': [
                {'date': 'Jan 1, 1863', 'text': 'The Emancipation Proclamation takes effect, declaring enslaved people in the rebelling states free.', 'order': 0, 'shuffle': 3},
                {'date': 'June 19, 1865', 'text': 'General Gordon Granger reads General Order No. 3 in Galveston, Texas.', 'order': 1, 'shuffle': 0},
                {'date': 'Dec 1865', 'text': 'The 13th Amendment ends slavery throughout the United States.', 'order': 2, 'shuffle': 5},
                {'date': '1872', 'text': 'Formerly enslaved leaders in Houston buy land for Emancipation Park to hold Juneteenth celebrations.', 'order': 3, 'shuffle': 1},
                {'date': '1979', 'text': 'Texas becomes the first state to make Juneteenth an official holiday.', 'order': 4, 'shuffle': 4},
                {'date': '2021', 'text': 'Juneteenth becomes a federal holiday across the United States.', 'order': 5, 'shuffle': 2},
            ],
        },
        'source': {'cite': 'Dates drawn from the U.S. National Archives and Texas History for Teachers (UNT).',
                   'links': [UNT_WS, NARA_13]},
        'answer_key': [
            'Order: 1863 Emancipation Proclamation → 1865 General Order No. 3 in Galveston → 1865 13th Amendment → 1872 Emancipation Park → 1979 Texas state holiday → 2021 federal holiday.',
        ],
        'discussion': [
            'Freedom was law in 1863 but reached Texas in 1865. Why might that gap matter?',
            'Why did people buy their own land to celebrate in 1872?',
            'What changed between the 1979 state holiday and the 2021 federal holiday?',
        ],
    },
    {
        'slug': 'photo-detective', 'band': '3–5', 'format': 'Identify, understand, connect',
        'title': 'Photo Detective',
        'card': 'Investigate a 1900 Emancipation Day photograph from Texas.',
        'intro': ('Historians read photographs like clues. Tap each prompt to investigate a 1900 Emancipation Day '
                  '(Juneteenth) celebration in Texas.'),
        'can': 'use details in a photograph to support an explanation.',
        'objective': 'Students analyze a primary-source photograph, distinguishing observation from inference.',
        'response': ('Write a caption using one detail you can actually see. Then write one question the photo leaves open.'),
        'hard_history': HH_35,
        'teks': {'code': '4.4(A)', 'se': 'Describe the impact of the Civil War and Reconstruction on Texas.'},
        'engine': {
            'type': 'reveal',
            'parts': [
                {'text': 'Identify: what do you see?', 'detail': ('A community band and crowd gathered for an Emancipation '
                                                                 'Day celebration in Texas, June 19, 1900 — 35 years after the Galveston announcement.')},
                {'text': 'Look closely: clothing and instruments', 'detail': ('People wear their best clothes and carry brass '
                                                                              'instruments. Celebrations often included music, parades, speeches, and shared meals.')},
                {'text': 'Understand: why a band?', 'detail': ('Public music and gathering were ways formerly enslaved families '
                                                              'and their descendants claimed freedom together, in public, with pride.')},
                {'text': 'Connect: then and now', 'detail': 'Many Texas communities still hold Juneteenth parades and music. What stays the same? What has changed?'},
                {'text': 'Ask: what is missing?', 'detail': 'A photo shows one moment from one view. Who is not in the frame? What questions does it leave open?'},
            ],
        },
        'source': {'cite': ('Emancipation Day celebration, June 19, 1900, Texas. Via The Portal to Texas History '
                            '(University of North Texas Libraries).'),
                   'links': [PORTAL]},
        'answer_key': [
            'Observations: a band, a crowd, formal clothing, an outdoor gathering.',
            'Inferences that need support: it is a celebration; people feel pride.',
            'A photograph cannot tell us names, sounds, or what happened before and after.',
        ],
        'discussion': [
            'What can a photograph prove, and what can it not prove?',
            'Why might a community dress in their best clothes for this day?',
            'What other sources would help you understand this celebration?',
        ],
    },
    {
        'slug': 'meet-opal-lee', 'band': '3–5', 'format': 'Profile card',
        'title': 'Meet Opal Lee',
        'card': 'Learn how one Texan helped make Juneteenth a national holiday.',
        'intro': 'Opal Lee is often called the “Grandmother of Juneteenth.” Tap each card to learn her story.',
        'can': 'explain how one person’s actions can help change a law.',
        'objective': 'Students explain how individual civic action contributed to a national holiday.',
        'response': 'What is one cause you would walk for? Write how you would try to make a change.',
        'hard_history': HH_35,
        'teks': {'code': '4.4(A) extension; 20th–21st century citizenship',
                 'se': 'Identify the contributions of individuals who shaped history.', 'verify': True},
        'engine': {
            'type': 'reveal',
            'parts': [
                {'text': 'Who she is', 'detail': 'Opal Lee is a retired teacher from Fort Worth, Texas, born in 1926. People call her the “Grandmother of Juneteenth.”'},
                {'text': 'Her idea', 'detail': 'She wanted Juneteenth to be a national holiday so the whole country would remember emancipation.'},
                {'text': 'Her walk', 'detail': ('Starting at age 89, she walked 2.5 miles in cities across the country — 2.5 miles '
                                               'for the 2.5 years between the Emancipation Proclamation and the news reaching Galveston.')},
                {'text': 'The petition', 'detail': 'She gathered more than a million signatures asking Congress to act.'},
                {'text': '2021', 'detail': 'In 2021, Juneteenth became a federal holiday, and Opal Lee stood with the president as he signed the law.'},
            ],
        },
        'source': {'cite': 'Based on reporting about Opal Lee’s campaign for a Juneteenth national holiday.',
                   'links': [OPAL]},
        'answer_key': [
            'Opal Lee, a retired Texas teacher, campaigned for years — with symbolic 2.5-mile walks and a petition of over a million signatures — and Juneteenth became a federal holiday in 2021.',
        ],
        'discussion': [
            'Why did she choose to walk 2.5 miles?',
            'How can ordinary people help change a law?',
            'What makes a goal worth working on for years?',
        ],
    },
    # ====================== 6–8 ======================
    {
        'slug': 'general-order-3', 'band': '6–8', 'format': 'Click to annotate',
        'title': 'General Order No. 3 Close Read',
        'card': 'Mark what the order announced, encouraged, and warned against.',
        'intro': ('On June 19, 1865, General Order No. 3 was read in Galveston. Read it closely. Choose a label, '
                  'then tap each part to mark what the order announced, what it encouraged, and what it warned against.'),
        'can': 'analyze a primary source and identify its parts and purpose.',
        'objective': ('Students analyze General Order No. 3, distinguishing its declaration from its instructions, '
                      'to explain social effects of the Civil War and Reconstruction in Texas.'),
        'response': ('The order announced freedom and equal rights. It also told freed people what to do and what not '
                     'to do. In two sentences, explain the tension between the promise and the instructions.'),
        'hard_history': HH_612,
        'teks': {'code': '7.5(C)', 'se': 'Explain the political, economic, and social effects of the Civil War and Reconstruction in Texas.'},
        'engine': {
            'type': 'annotate',
            'tags': ['Announced (what it declared)', 'Encouraged (what it advised)', 'Warned (what it told people not to do)'],
            'segments': [
                {'text': 'The people of Texas are informed that, in accordance with a proclamation from the Executive of the United States, all slaves are free.', 'tag': 0},
                {'text': 'This involves an absolute equality of personal rights and rights of property between former masters and slaves,', 'tag': 0},
                {'text': 'and the connection heretofore existing between them becomes that between employer and hired labor.', 'tag': 1},
                {'text': 'The freedmen are advised to remain quietly at their present homes and work for wages.', 'tag': 1},
                {'text': 'They are informed that they will not be allowed to collect at military posts,', 'tag': 2},
                {'text': 'and that they will not be supported in idleness either there or elsewhere.', 'tag': 2},
            ],
        },
        'source': {'quote': GO3_TEXT, 'cite': GO3_CITE, 'links': [NARA_GO3, UNT_LESSON]},
        'answer_key': [
            'Announced: “all slaves are free” and “an absolute equality of personal rights and rights of property.”',
            'Encouraged: the relationship becomes “employer and hired labor”; freed people are “advised to remain quietly… and work for wages.”',
            'Warned: they “will not be allowed to collect at military posts” and “will not be supported in idleness.”',
        ],
        'discussion': [
            'The order promised “absolute equality,” then told freed people to stay and work for wages. Why might that feel like a mixed message?',
            'Who benefited from freed people remaining on the same farms?',
            'Freedom was announced in Texas 2.5 years after the Emancipation Proclamation. Why did the news take so long?',
        ],
    },
    {
        'slug': 'news-delay', 'band': '6–8', 'format': 'Trace the timeline',
        'title': 'The News Delay',
        'card': 'Trace how word of freedom reached Galveston — and ask who gained from the delay.',
        'intro': ('Freedom was law long before it reached everyone. Put the steps in order to trace how — and how '
                  'slowly — the news of freedom traveled to Texas.'),
        'can': 'explain cause and effect and why news of freedom was delayed.',
        'objective': 'Students trace cause and effect in the delayed enforcement of emancipation in Texas.',
        'response': ('The Emancipation Proclamation took effect in 1863, but Texans were not freed until June 1865. '
                     'Explain one reason for the delay and name who gained from it.'),
        'hard_history': HH_612,
        'teks': {'code': '7.5(C), 8.1(A)',
                 'se': 'Explain effects of the Civil War and Reconstruction; identify causes and effects of major eras through 1877.'},
        'engine': {
            'type': 'sequence',
            'items': [
                {'date': 'Sep 1862', 'text': 'President Lincoln issues the preliminary Emancipation Proclamation.', 'order': 0, 'shuffle': 1},
                {'date': 'Jan 1863', 'text': 'The Proclamation takes effect — but it can be enforced only where the U.S. Army has reached.', 'order': 1, 'shuffle': 4},
                {'date': '1863–64', 'text': 'Some enslavers move people to Texas, far from Union lines, to keep them enslaved.', 'order': 2, 'shuffle': 0},
                {'date': 'Apr 1865', 'text': 'The Confederacy surrenders; the Civil War ends.', 'order': 3, 'shuffle': 3},
                {'date': 'June 1865', 'text': 'U.S. Army troops under General Granger reach Galveston and announce freedom.', 'order': 4, 'shuffle': 2},
            ],
        },
        'source': {'cite': 'Based on the PBS NewsHour Classroom lesson on the history of Juneteenth.',
                   'links': [PBS, NARA_EP]},
        'answer_key': [
            'Order: preliminary Proclamation (1862) → Proclamation takes effect (1863) → enslavers move people to Texas (1863–64) → Confederate surrender (Apr 1865) → Galveston announcement (June 1865).',
            'The Proclamation freed people only where the Army could enforce it; Texas was distant, and some enslavers moved people there to avoid Union control. Enslavers gained free labor during the 2.5-year delay.',
        ],
        'discussion': [
            'Why was a law not enough to make people free in practice?',
            'Who had an interest in keeping the news from spreading?',
            'How does this delay connect to why Juneteenth is remembered?',
        ],
    },
    {
        'slug': 'proclamation-to-galveston', 'band': '6–8', 'format': 'Breakout challenge',
        'title': 'Proclamation to Galveston',
        'card': 'Crack each lock using cause-and-effect clues from 1863 to 1865.',
        'intro': ('Open each lock in order. Use the evidence and cause-and-effect reasoning to choose each answer. '
                  'A correct answer opens the next lock.'),
        'can': 'use cause-and-effect evidence to reach a conclusion.',
        'objective': 'Students sequence cause and effect from the Emancipation Proclamation to Juneteenth.',
        'response': 'In one sentence, state the cause and the effect that this chain of events shows.',
        'hard_history': HH_612,
        'teks': {'code': '8.1(A)', 'se': 'Identify the major eras in U.S. history through 1877 and their causes and effects.'},
        'engine': {
            'type': 'breakout',
            'locks': [
                {'clue': 'Lock 1 — When did the Emancipation Proclamation take effect?',
                 'prompt': 'Choose the year.',
                 'choices': [{'text': '1861', 'val': 'a'}, {'text': '1863', 'val': 'b'}, {'text': '1865', 'val': 'c'}],
                 'answer': 'b', 'reveal': 'Correct. But the Proclamation could free people only where the U.S. Army had reached.'},
                {'clue': 'Lock 2 — Why could the Proclamation not immediately free people in Texas?',
                 'prompt': 'Choose the best reason.',
                 'choices': [{'text': 'Texas was far from Union lines, so the order could not be enforced there.', 'val': 'a'},
                             {'text': 'Texas had already ended slavery on its own.', 'val': 'b'},
                             {'text': 'The Proclamation did not apply to Texas at all.', 'val': 'c'}],
                 'answer': 'a', 'reveal': 'Right. Enforcement needed U.S. troops on the ground.'},
                {'clue': 'Lock 3 — In what city was General Order No. 3 read on June 19, 1865?',
                 'prompt': 'Choose the city.',
                 'choices': [{'text': 'Galveston', 'val': 'a'}, {'text': 'Austin', 'val': 'b'}, {'text': 'Dallas', 'val': 'c'}],
                 'answer': 'a', 'reveal': 'Yes — General Gordon Granger announced freedom in Galveston.'},
                {'clue': 'Lock 4 — How long after the Proclamation took effect did freedom reach Galveston?',
                 'prompt': 'Choose the closest answer.',
                 'choices': [{'text': 'About 2.5 years', 'val': 'a'}, {'text': 'About 6 months', 'val': 'b'}, {'text': 'About 10 years', 'val': 'c'}],
                 'answer': 'a', 'reveal': 'Correct. That 2.5-year gap is why Opal Lee’s symbolic walks are 2.5 miles.'},
            ],
        },
        'source': {'cite': 'Clues based on the PBS NewsHour Classroom and DocsTeach Juneteenth lessons.',
                   'links': [PBS, DOCSTEACH]},
        'answer_key': [
            'Chain: 1863 (law) → distance and the need for enforcement → Galveston, June 19, 1865 → a gap of about 2.5 years.',
        ],
        'discussion': [
            'Which link in the chain was the true cause of the delay?',
            'How is “freedom on paper” different from “freedom enforced”?',
            'What evidence would you add to make the chain stronger?',
        ],
    },
    {
        'slug': 'celebration-then-and-now', 'band': '6–8', 'format': 'Compare and contrast',
        'title': 'Celebration Then and Now',
        'card': 'Sort how Juneteenth was marked in the 1800s and how Texans mark it today.',
        'intro': ('Juneteenth celebrations have both changed and stayed the same. Sort each tradition into Then '
                  '(1860s–1900), Now (today), or Both.'),
        'can': 'compare past and present and explain continuity and change.',
        'objective': 'Students analyze continuity and change in Juneteenth commemoration.',
        'response': 'Name one thing that stayed the same and one thing that changed. Explain why the change happened.',
        'hard_history': HH_612,
        'teks': {'code': '7.5(C)', 'se': 'Explain the political, economic, and social effects of the Civil War and Reconstruction in Texas.'},
        'engine': {
            'type': 'sort',
            'buckets': [{'id': 'then', 'text': 'Then (1860s–1900)'},
                        {'id': 'now', 'text': 'Now (today)'},
                        {'id': 'both', 'text': 'Both'}],
            'items': [
                {'text': 'Reading General Order No. 3 aloud', 'cat': 'both'},
                {'text': 'Prayer services and speeches', 'cat': 'both'},
                {'text': 'Buying private land for celebrations because segregation barred public parks (Emancipation Park, 1872)', 'cat': 'then'},
                {'text': 'Brass bands and parades', 'cat': 'both'},
                {'text': 'Festivals streamed online and shared on social media', 'cat': 'now'},
                {'text': 'A paid day off as a state and federal holiday', 'cat': 'now'},
            ],
        },
        'source': {'cite': 'Based on the Texas Today lesson and worksheet (UNT, Texas History for Teachers).',
                   'links': [UNT_WS, UNT_LESSON]},
        'answer_key': [
            'Then: buying private land because segregation barred public parks.',
            'Now: online festivals; a paid state and federal holiday.',
            'Both: reading General Order No. 3 aloud; prayer and speeches; bands and parades; shared meals.',
        ],
        'discussion': [
            'Which traditions carried across 150 years, and why do you think they lasted?',
            'Why did early celebrations often happen on privately owned land?',
            'What does becoming a paid holiday change about how people observe the day?',
        ],
    },
    # ====================== 9–12 ======================
    {
        'slug': 'meaning-of-freedom', 'band': '9–12', 'format': 'Document-based inquiry',
        'title': 'The Meaning of Freedom',
        'card': 'Weigh the order’s promises of freedom against its limits on that freedom.',
        'intro': ('General Order No. 3 announced freedom — and set conditions on it. Choose a label, then mark each '
                  'clause as a promise of freedom or a limit on it. Then weigh the two in your response.'),
        'can': 'analyze a document, qualify a claim with evidence, and state a limitation.',
        'objective': 'Students construct an evidence-based interpretation of the meaning of freedom in June 1865.',
        'response': ('Write a thesis: did General Order No. 3 deliver freedom, or a conditional freedom? Use two clauses '
                     'as evidence, and name one limitation of relying on this single document.'),
        'hard_history': HH_612,
        'teks': {'code': 'U.S. History Since 1877 (§113.41)',
                 'se': 'Analyze primary sources; evaluate the meaning and limits of emancipation.', 'verify': True},
        'engine': {
            'type': 'annotate',
            'tags': ['Promise of freedom', 'Limit on that freedom'],
            'segments': [
                {'text': 'all slaves are free.', 'tag': 0},
                {'text': 'This involves an absolute equality of personal rights and rights of property between former masters and slaves,', 'tag': 0},
                {'text': 'the connection heretofore existing between them becomes that between employer and hired labor.', 'tag': 1},
                {'text': 'The freedmen are advised to remain quietly at their present homes and work for wages.', 'tag': 1},
                {'text': 'they will not be allowed to collect at military posts,', 'tag': 1},
                {'text': 'and that they will not be supported in idleness either there or elsewhere.', 'tag': 1},
            ],
        },
        'source': {'quote': GO3_TEXT, 'cite': GO3_CITE, 'links': [NARA_GO3, PBS, DOCSTEACH]},
        'answer_key': [
            'Promise: “all slaves are free”; “an absolute equality of personal rights and rights of property.”',
            'Limit: recasting the relationship as “employer and hired labor”; “remain quietly… and work for wages”; no gathering at military posts; no support “in idleness.”',
            'A strong response notes that true equality required the 13th and 14th Amendments and enforcement that this order alone did not guarantee.',
        ],
        'discussion': [
            'What did “freedom” legally mean in June 1865, and what did it not yet guarantee?',
            'How do the labor instructions reveal the limits of emancipation before the 13th and 14th Amendments?',
            'Whose interests did “remain quietly and work for wages” serve?',
        ],
    },
    {
        'slug': 'holiday-case', 'band': '9–12', 'format': 'Evidence-based argument',
        'title': 'The Holiday Case',
        'card': 'Build the evidence-based case for why Juneteenth became a federal holiday.',
        'intro': ('Lawmakers weigh evidence before they act. Work through each question to assemble the strongest '
                  'case for Juneteenth as a national holiday. A correct choice opens the next step.'),
        'can': 'select evidence and build a reasoned historical argument.',
        'objective': 'Students construct an evidence-based argument that anticipates a counterargument.',
        'response': ('Write a one-paragraph argument — claim, two pieces of evidence, and a response to one counterargument '
                     '— on why Juneteenth became a federal holiday in 2021.'),
        'hard_history': HH_612,
        'teks': {'code': 'U.S. History Since 1877 (§113.41)',
                 'se': 'Construct and defend an argument using historical evidence.', 'verify': True},
        'engine': {
            'type': 'breakout',
            'locks': [
                {'clue': 'Step 1 — Which is a thesis a historian could defend with evidence?',
                 'prompt': 'Choose the defensible claim.',
                 'choices': [{'text': 'Juneteenth marks the end of enforced slavery in the last Confederate state and belongs in the national memory of emancipation.', 'val': 'a'},
                             {'text': 'Juneteenth is simply the best holiday.', 'val': 'b'},
                             {'text': 'Everyone enjoys a day off.', 'val': 'c'}],
                 'answer': 'a', 'reveal': 'A thesis makes a specific, defensible claim.'},
                {'clue': 'Step 2 — Which evidence best supports making Juneteenth national, not only in Texas?',
                 'prompt': 'Choose the strongest evidence.',
                 'choices': [{'text': 'Emancipation was a national event; the 13th Amendment ended slavery across the whole country in 1865.', 'val': 'a'},
                             {'text': 'Texas has good weather in June.', 'val': 'b'},
                             {'text': 'Opal Lee happens to be from Texas.', 'val': 'c'}],
                 'answer': 'a', 'reveal': 'Strong evidence ties the local event to a national meaning.'},
                {'clue': 'Step 3 — Which counterargument should the case answer?',
                 'prompt': 'Choose the serious objection.',
                 'choices': [{'text': 'Some argue freedom was already law in 1863, so June 19 is only symbolic.', 'val': 'a'},
                             {'text': 'Some argue June is too hot for a holiday.', 'val': 'b'}],
                 'answer': 'a', 'reveal': 'A strong argument anticipates and answers real objections.'},
                {'clue': 'Step 4 — Why commemorate June 19 even though emancipation was law in 1863?',
                 'prompt': 'Choose the best response to the counterargument.',
                 'choices': [{'text': 'It marks when freedom was finally enforced for the last enslaved people — the gap between law and reality.', 'val': 'a'},
                             {'text': 'There is no good reason; it is purely symbolic.', 'val': 'b'}],
                 'answer': 'a', 'reveal': 'Commemoration marks enforcement and memory, not only the date a law passed.'},
            ],
        },
        'source': {'cite': 'Based on the DocsTeach Juneteenth General Order lesson and the National Archives.',
                   'links': [DOCSTEACH, NARA_13]},
        'answer_key': [
            'Thesis: Juneteenth marks the enforcement of emancipation in the last Confederate state and belongs in national memory.',
            'Evidence: emancipation was national; the 13th Amendment (1865) ended slavery everywhere.',
            'Counterargument answered: though freedom was law in 1863, June 19 marks when it was finally enforced — the gap between law and reality.',
        ],
        'discussion': [
            'What distinguishes a defensible thesis from an opinion?',
            'Why is answering a counterargument part of a strong argument?',
            'What additional evidence would strengthen the case for a federal holiday?',
        ],
    },
    {
        'slug': 'commemoration-map', 'band': '9–12', 'format': 'Map and timeline',
        'title': 'Commemoration Map',
        'card': 'Place documented Juneteenth milestones across Texas and the nation over time.',
        'intro': ('Juneteenth spread outward from one Texas city. Place each milestone in the region where it happened '
                  'to map how commemoration grew across Texas and the nation.'),
        'can': 'place events in space and time and describe how commemoration spread.',
        'objective': 'Students map the spatial and temporal spread of Juneteenth commemoration.',
        'response': 'Describe the pattern: where did Juneteenth begin, and how did commemoration spread across Texas and the nation over time?',
        'hard_history': HH_612,
        'teks': {'code': 'U.S. History Since 1877 (§113.41)',
                 'se': 'Create and interpret maps and locate events in time and place.', 'verify': True},
        'engine': {
            'type': 'sort', 'map': True,
            'buckets': [{'id': 'galv', 'text': 'Galveston (Gulf Coast)'},
                        {'id': 'hou', 'text': 'Houston'},
                        {'id': 'aus', 'text': 'Austin (Central Texas)'},
                        {'id': 'dc', 'text': 'Washington, D.C. (national)'}],
            'items': [
                {'text': '1865 — General Order No. 3 is read, announcing freedom.', 'cat': 'galv'},
                {'text': '1867 — Freedmen organize some of the earliest Emancipation Day celebrations in the capital.', 'cat': 'aus'},
                {'text': '1872 — Formerly enslaved leaders buy land for Emancipation Park.', 'cat': 'hou'},
                {'text': '1979 — The Texas Legislature makes Juneteenth a state holiday.', 'cat': 'aus'},
                {'text': '2021 — Juneteenth becomes a federal holiday.', 'cat': 'dc'},
            ],
        },
        'source': {'cite': 'Milestones drawn from The Portal to Texas History and the U.S. National Archives.',
                   'links': [PORTAL, NARA_13]},
        'answer_key': [
            'Galveston: 1865 announcement. Austin: 1867 early celebrations and the 1979 state holiday. Houston: 1872 Emancipation Park. Washington, D.C.: 2021 federal holiday.',
            'Pattern: it began in Galveston (1865), took root in Houston and Austin (1860s–1870s), became a Texas holiday from the capital (1979), and went national (2021).',
        ],
        'discussion': [
            'Why did commemoration begin on the Gulf Coast and move inland?',
            'What does the move from private parks to a federal holiday show about changing recognition?',
            'How does mapping events in place and time deepen your understanding of the spread?',
        ],
    },
]
