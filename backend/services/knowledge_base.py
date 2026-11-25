"""Offline bilingual knowledge base covering all 38 PlantVillage classes with weather/soil rules."""

from typing import Any, Dict, List, Optional


def _entry(
    friendly_name: str,
    en_summary: str,
    en_chemical: List[str],
    en_organic: List[str],
    en_prevention: List[str],
    en_safety: List[str],
    hi_summary: str,
    hi_chemical: List[str],
    hi_organic: List[str],
    hi_prevention: List[str],
    hi_safety: List[str],
    store_categories: List[str],
    shopping_items: List[str],
) -> Dict[str, Any]:
    return {
        "friendly_name": friendly_name,
        "store_categories": store_categories,
        "shopping_items": shopping_items,
        "english": {
            "summary": en_summary,
            "chemical": en_chemical,
            "organic": en_organic,
            "prevention": en_prevention,
            "safety": en_safety,
        },
        "hindi": {
            "summary": hi_summary,
            "chemical": hi_chemical,
            "organic": hi_organic,
            "prevention": hi_prevention,
            "safety": hi_safety,
        },
    }


def _healthy_entry(crop_en: str, crop_hi: str) -> Dict[str, Any]:
    return _entry(
        friendly_name=f"{crop_en} - Healthy",
        en_summary=f"Your {crop_en.lower()} leaf looks healthy with no visible disease symptoms.",
        en_chemical=["No chemical pesticide spray needed right now."],
        en_organic=[
            "Apply well-rotted farmyard manure or vermicompost around the root zone.",
            "Optional preventive spray of 1–2% neem oil every 15 days.",
        ],
        en_prevention=[
            "Water at the base in the morning and avoid waterlogging.",
            "Inspect leaf undersides weekly for early pest or fungal signs.",
        ],
        en_safety=["Avoid unnecessary chemical sprays to protect pollinators and soil microbes."],
        hi_summary=f"आपकी {crop_hi} की पत्ती स्वस्थ दिख रही है और रोग के कोई लक्षण नहीं हैं।",
        hi_chemical=["अभी किसी रासायनिक कीटनाशक के छिड़काव की आवश्यकता नहीं है।"],
        hi_organic=[
            "जड़ों के पास अच्छी सड़ी गोबर खाद या वर्मीकम्पोस्ट डालें।",
            "रोकथाम के लिए हर 15 दिन में 1–2% नीम तेल का छिड़काव कर सकते हैं।",
        ],
        hi_prevention=[
            "सुबह के समय जड़ों के पास सिंचाई करें और जलभराव से बचें।",
            "सप्ताह में एक बार पत्तियों के निचले हिस्से की जांच करें।",
        ],
        hi_safety=["मित्र कीटों और मिट्टी की सेहत बचाने के लिए अनावश्यक रसायन न छिड़कें।"],
        store_categories=["manure", "fertilizers"],
        shopping_items=["Vermicompost / Organic Manure", "Balanced NPK Fertilizer", "Neem Oil (Preventive)"],
    )


DISEASE_INFO: Dict[str, Dict[str, Any]] = {
    "Apple___Apple_scab": _entry(
        "Apple - Apple Scab",
        "Fungal disease causing olive-green to dark scabby lesions on leaves and fruits in cool, wet weather.",
        ["Use protectant fungicide from Mancozeb or Captan group.", "For severe spread, rotate with a Triazole or Strobilurin group fungicide."],
        ["Spray 2% neem oil or wettable sulfur (if temperatures are below 30°C).", "Apply compost tea and prune dense canopy for airflow."],
        ["Rake and compost/destroy fallen infected leaves.", "Prune trees in winter to open the canopy."],
        ["Wear gloves, goggles, and mask during spraying.", "Do not spray near water bodies."],
        "सेब में स्कैब फफूंद के कारण पत्तियों और फलों पर जैतून-हरे या काले दाग बनते हैं।",
        ["मैनकोजेब या कैप्टान समूह के फफूंदनाशक का उपयोग करें।", "अधिक फैलाव होने पर ट्रायज़ोल या स्ट्रोबिल्यूरिन समूह से बदलाव करें।"],
        ["2% नीम तेल या घुलनशील सल्फर (30°C से कम तापमान पर) का छिड़काव करें।", "हवा के प्रवाह के लिए घनी टहनियों की छंटाई करें।"],
        ["गिरे हुए संक्रमित पत्तों को खेत से हटाकर नष्ट करें।", "सर्दियों में उचित छंटाई करें।"],
        ["छिड़काव के समय दस्ताने, चश्मा और मास्क पहनें।", "जल स्रोतों के पास छिड़काव न करें।"],
        ["pesticides", "fertilizers"],
        ["Mancozeb / Captan Fungicide", "Wettable Sulfur", "Neem Oil"],
    ),
    "Apple___Black_rot": _entry(
        "Apple - Black Rot",
        "Black rot affects leaves, bark, and fruits, producing frog-eye leaf spots and black mummified fruit.",
        ["Use Copper oxychloride or Captan group fungicides at early bud/leaf stage."],
        ["Prune out dead cankers and infected twigs.", "Apply neem + cow urine bio-spray and enrich soil with vermicompost."],
        ["Remove mummified fruits from trees and orchard floor.", "Disinfect pruning shears between cuts."],
        ["Wear protective eyewear and rubber gloves.", "Follow pre-harvest waiting intervals."],
        "ब्लैक रॉट से पत्तियों पर दाग पड़ते हैं और फल काले होकर सूख जाते हैं।",
        ["कॉपर ऑक्सीक्लोराइड या कैप्टान समूह की फफूंदनाशक दवा का उपयोग करें।"],
        ["सूखी व संक्रमित टहनियाँ काटकर हटाएँ।", "नीम + गोमूत्र घोल छिड़कें और वर्मीकम्पोस्ट से मिट्टी सुधारें।"],
        ["पेड़ पर लटके सड़े फलों को तुरंत हटाएँ।", "छंटाई वाले औज़ारों को सैनिटाइज करें।"],
        ["दस्ताने और सुरक्षा चश्मा पहनें।", "तुड़ाई से पहले प्रतीक्षा अवधि का पालन करें।"],
        ["pesticides", "manure"],
        ["Copper Oxychloride Fungicide", "Vermicompost", "Neem Oil"],
    ),
    "Apple___Cedar_apple_rust": _entry(
        "Apple - Cedar Apple Rust",
        "Fungal rust producing bright orange-yellow spots on apple leaves, cycling between apple and juniper/cedar trees.",
        ["Apply fungicide from Mancozeb or Myclobutanil (Triazole) group at pink-bud to petal-fall stage."],
        ["Apply sulfur-based organic fungicide early in the season.", "Support tree vigor with organic compost and potash."],
        ["Remove nearby wild cedar/juniper galls if feasible.", "Plant rust-resistant apple cultivars."],
        ["Wear mask and avoid spraying during windy hours.", "Keep livestock away from freshly sprayed orchards."],
        "सीडर एप्पल रस्ट में पत्तियों पर चमकीले नारंगी धब्बे बनते हैं जो जूनीपर/सीडर पेड़ों से फैलते हैं।",
        ["मैनकोजेब या ट्रायज़ोल (माइक्लोबुटानिल) समूह की दवा का छिड़काव करें।"],
        ["शुरुआती अवस्था में सल्फर आधारित जैविक छिड़काव करें।", "जैविक खाद व पोटाश से पेड़ की रोग-रोधी क्षमता बढ़ाएँ।"],
        ["आसपास के जंगली जूनीपर पौधों की छंटाई करें।", "रोग-रोधी किस्में लगाएँ।"],
        ["तेज हवा में स्प्रे न करें और मास्क पहनें।", "पशुओं को ताजे छिड़काव वाले क्षेत्र से दूर रखें।"],
        ["pesticides", "fertilizers"],
        ["Mancozeb / Triazole Fungicide", "Wettable Sulfur", "Organic Compost & Potash"],
    ),
    "Apple___healthy": _healthy_entry("Apple", "सेब"),
    "Blueberry___healthy": _healthy_entry("Blueberry", "ब्लूबेरी"),
    "Cherry_(including_sour)___Powdery_mildew": _entry(
        "Cherry - Powdery Mildew",
        "White powdery fungal coating on young cherry leaves and shoots, curling leaves in warm, humid conditions.",
        ["Use wettable Sulfur or Triazole/Strobilurin group fungicides with rotation."],
        ["Spray 2% neem oil or potassium bicarbonate solution.", "Apply compost mulch to keep root moisture steady."],
        ["Prune crowded shoots to improve sunlight and airflow.", "Avoid excess nitrogen fertilizer."],
        ["Do not mix sulfur with oils within 14 days.", "Wear PPE while spraying."],
        "चेरी के पाउडरी मिल्ड्यू में नई पत्तियों पर सफेद पाउडर जैसी परत जम जाती है।",
        ["घुलनशील सल्फर या ट्रायज़ोल/स्ट्रोबिल्यूरिन समूह के फफूंदनाशक का बदल-बदल कर उपयोग करें।"],
        ["2% नीम तेल या पोटैशियम बाइकार्बोनेट का छिड़काव करें।", "जड़ों के पास कम्पोस्ट मल्च लगाएँ।"],
        ["हवा और धूप के लिए अतिरिक्त टहनियों की छंटाई करें।", "अधिक नाइट्रोजन खाद न डालें।"],
        ["तेल और सल्फर को 14 दिनों के भीतर साथ न मिलाएँ।", "छिड़काव के समय सुरक्षा किट पहनें।"],
        ["pesticides", "manure"],
        ["Wettable Sulfur", "Neem Oil", "Organic Compost Mulch"],
    ),
    "Cherry_(including_sour)___healthy": _healthy_entry("Cherry", "चेरी"),
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": _entry(
        "Corn (Maize) - Gray Leaf Spot",
        "Rectangular gray-to-tan lesions bounded by leaf veins, reducing photosynthesis during warm humid weather.",
        ["Apply Strobilurin + Triazole combination fungicide if lesions reach ear leaf."],
        ["Use Trichoderma viride soil/foliar bio-fungicide.", "Side-dress with well-decomposed farmyard manure and balanced potash."],
        ["Rotate corn with legumes/soybean.", "Till or remove infected crop residue after harvest."],
        ["Wear mask and long sleeves in tall maize crops.", "Avoid spraying before heavy rain."],
        "मक्का का ग्रे लीफ स्पॉट पत्तियों की नसों के बीच आयताकार भूरे-स्लेटी धब्बे बनाता है।",
        ["रोग बढ़ने पर स्ट्रोबिल्यूरिन + ट्रायज़ोल समूह की दवा का छिड़काव करें।"],
        ["ट्राइकोडर्मा विरिडी जैव-फफूंदनाशक का प्रयोग करें।", "सड़ी गोबर खाद और संतुलित पोटाश दें।"],
        ["मक्का के बाद दलहन/सोयाबीन का फसल चक्र अपनाएँ।", "कटाई के बाद रोगग्रस्त अवशेष नष्ट करें।"],
        ["ऊंची फसल में छिड़काव करते समय मास्क और पूरी बांह के कपड़े पहनें।"],
        ["pesticides", "fertilizers", "manure"],
        ["Strobilurin / Triazole Fungicide", "Trichoderma Bio-fungicide", "Potash & Farmyard Manure"],
    ),
    "Corn_(maize)___Common_rust_": _entry(
        "Corn (Maize) - Common Rust",
        "Cinnamon-brown pustules on both leaf surfaces that rupture to release wind-borne rust spores.",
        ["Use Triazole or Strobilurin group fungicide only if infection is severe before tasseling."],
        ["Apply neem oil + Pseudomonas fluorescens bio-spray.", "Maintain balanced NPK with organic compost."],
        ["Plant rust-resistant hybrid maize seeds.", "Avoid excessive nitrogen application."],
        ["Spray in the direction of the wind.", "Keep grazing animals away from treated fields."],
        "मक्का के कॉमन रस्ट में पत्तियों की दोनों सतहों पर भूरे-लाल फफोले बनते हैं।",
        ["फूल आने से पहले रोग गंभीर होने पर ट्रायज़ोल या स्ट्रोबिल्यूरिन समूह की दवा छिड़कें।"],
        ["नीम तेल और स्यूडोमोनास जैव-उपचार का उपयोग करें।", "जैविक खाद के साथ संतुलित NPK दें।"],
        ["रस्ट-प्रतिरोधी मक्का किस्मों की बुवाई करें।", "अत्यधिक नाइट्रोजन यूरिया न डालें।"],
        ["हवा की दिशा देखकर छिड़काव करें और पशुओं को दूर रखें।"],
        ["pesticides", "fertilizers"],
        ["Triazole Fungicide", "Balanced NPK Fertilizer", "Neem Bio-spray"],
    ),
    "Corn_(maize)___Northern_Leaf_Blight": _entry(
        "Corn (Maize) - Northern Leaf Blight",
        "Long cigar-shaped gray-green lesions on lower leaves moving upward in cool, wet, or dewy weather.",
        ["Use Azoxystrobin (Strobilurin) or Propiconazole (Triazole) group fungicide when upper leaves are threatened."],
        ["Spray Trichoderma-enriched bio-formulation or neem extract.", "Strengthen crop with compost + zinc sulfate if deficient."],
        ["Rotate crops and plow under old corn stalks.", "Choose resistant hybrids."],
        ["Follow label dosage and wear protective mask and gloves."],
        "नॉर्दर्न लीफ ब्लाइट में मक्का की पत्तियों पर सिगार के आकार के लंबे स्लेटी धब्बे बनते हैं।",
        ["ऊपरी पत्तियों के बचाव के लिए स्ट्रोबिल्यूरिन या ट्रायज़ोल समूह का फफूंदनाशक उपयोग करें।"],
        ["ट्राइकोडर्मा जैव-नियंत्रक और नीम अर्क का प्रयोग करें।", "कम्पोस्ट और जिंक सल्फेट से फसल को मजबूत करें।"],
        ["फसल चक्र अपनाएँ और पुराने डंठल खेत से हटाएँ।", "प्रतिरोधी किस्म चुनें।"],
        ["निर्धारित मात्रा का पालन करें तथा मास्क व दस्ताने पहनें।"],
        ["pesticides", "fertilizers"],
        ["Strobilurin / Triazole Fungicide", "Trichoderma Bio-control", "Zinc Sulfate & Compost"],
    ),
    "Corn_(maize)___healthy": _healthy_entry("Corn (Maize)", "मक्का"),
    "Grape___Black_rot": _entry(
        "Grape - Black Rot",
        "Fungal infection causing tan circular leaf spots with black borders and shriveled black mummified berries.",
        ["Apply Copper oxychloride, Mancozeb, or Strobilurin group fungicide from bud-break through fruit set."],
        ["Remove infected clusters immediately.", "Spray neem solution or Trichoderma bio-fungicide and apply vermicompost."],
        ["Train and prune vines for strong airflow.", "Avoid late-evening overhead irrigation."],
        ["Wear rubber gloves and wash sprayers thoroughly after use."],
        "अंगूर के ब्लैक रॉट में पत्तियों पर भूरे दाग पड़ते हैं और अंगूर के दाने काले होकर सिकुड़ जाते हैं।",
        ["कॉपर ऑक्सीक्लोराइड, मैनकोजेब या स्ट्रोबिल्यूरिन समूह की दवा का छिड़काव करें।"],
        ["संक्रमित गुच्छों को तुरंत हटाएँ।", "नीम घोल या ट्राइकोडर्मा छिड़कें और वर्मीकम्पोस्ट दें।"],
        ["बेलों की छंटाई कर हवा का प्रवाह बढ़ाएँ।", "शाम के समय ऊपर से पानी न दें।"],
        ["रबर के दस्ताने पहनें और उपयोग के बाद स्प्रेयर धोएँ।"],
        ["pesticides", "manure"],
        ["Copper Oxychloride / Mancozeb", "Trichoderma Bio-fungicide", "Vermicompost"],
    ),
    "Grape___Esca_(Black_Measles)": _entry(
        "Grape - Esca (Black Measles)",
        "Vascular wood-decay complex causing tiger-stripe leaf discoloration and dark spotting on grape berries.",
        ["Protect fresh pruning wounds with Copper-based paste or Thiophanate-methyl fungicide paste."],
        ["Apply Trichoderma harzianum paste on pruning cuts.", "Improve soil organic matter with well-rotted FYM and seaweed/humic extract."],
        ["Prune during dry weather and disinfect tools.", "Remove severely dead wood and burn/dispose away from vineyard."],
        ["Avoid chemical runoff into irrigation channels; wear gloves when applying wound paste."],
        "एस्का (ब्लैक मीज़ल्स) में अंगूर की पत्तियों पर बाघ जैसी धारियाँ और दानों पर काले धब्बे दिखते हैं।",
        ["छंटाई के ताजे घावों पर कॉपर आधारित पेस्ट या फफूंदनाशक लेप लगाएँ।"],
        ["कटे हुए हिस्सों पर ट्राइकोडर्मा हार्ज़ियानम पेस्ट लगाएँ।", "सड़ी गोबर खाद और ह्यूमिक जैविक खाद से जड़ें मजबूत करें।"],
        ["सूखे मौसम में छंटाई करें और औज़ार साफ रखें।", "मृत लकड़ी हटाकर नष्ट करें।"],
        ["पेस्ट लगाते समय दस्ताने पहनें और रसायन नालियों में न बहाएँ।"],
        ["pesticides", "manure"],
        ["Copper Wound Paste", "Trichoderma Bio-paste", "Farmyard Manure & Humic Acid"],
    ),
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": _entry(
        "Grape - Leaf Blight",
        "Irregular dark-brown to reddish leaf spots that coalesce, causing premature defoliation.",
        ["Spray Mancozeb or Copper oxychloride group fungicide at 10–14 day intervals."],
        ["Use 2% neem oil + wood-ash/compost tea foliar support.", "Enrich root zone with organic compost."],
        ["Improve trellis ventilation and avoid dense foliage.", "Clear fallen leaves after season."],
        ["Respect pre-harvest interval and wear mask/gloves."],
        "अंगूर के लीफ ब्लाइट में पत्तियों पर गहरे भूरे-लाल धब्बे बनकर पत्तियाँ समय से पहले गिरने लगती हैं।",
        ["मैनकोजेब या कॉपर ऑक्सीक्लोराइड समूह के फफूंदनाशक का 10–14 दिन पर छिड़काव करें।"],
        ["2% नीम तेल और कम्पोस्ट टी का उपयोग करें।", "जड़ों में जैविक खाद मिलाएँ।"],
        ["लताओं पर हवा की निकासी सुधारें और गिरे पत्ते साफ करें।"],
        ["तुड़ाई से पहले प्रतीक्षा अवधि का ध्यान रखें और मास्क पहनें।"],
        ["pesticides", "manure"],
        ["Mancozeb / Copper Fungicide", "Neem Oil", "Organic Compost"],
    ),
    "Grape___healthy": _healthy_entry("Grape", "अंगूर"),
    "Orange___Haunglongbing_(Citrus_greening)": _entry(
        "Orange - Citrus Greening (HLB)",
        "Bacterial disease spread by citrus psyllids causing blotchy yellow leaf mottling and bitter, lopsided fruit. No chemical cure exists once systemic.",
        ["Control the vector (Asian citrus psyllid) using systemic/contact Insecticide groups (Imidacloprid or Pyrethroid rotation)."],
        ["Spray neem oil + horticultural soap to repel psyllids.", "Boost tree resilience with micronutrient mix (Zinc, Boron, Iron) and vermicompost."],
        ["Remove severely infected trees to save healthy orchard trees.", "Use certified disease-free nursery saplings."],
        ["Never inject unapproved antibiotics; protect honeybees by avoiding sprays during flowering."],
        "सिट्रस ग्रीनिंग (HLB) साइलिड कीट से फैलने वाला जीवाणु रोग है जिससे पत्तियाँ धब्बेदार पीली पड़ती हैं।",
        ["रोग फैलाने वाले साइलिड कीट के नियंत्रण हेतु अनुशंसित कीटनाशक समूह (इमिडाक्लोप्रिड/पायरेथ्रॉइड बदलकर) उपयोग करें।"],
        ["साइलिड भगाने के लिए नीम तेल का छिड़काव करें।", "जिंक, बोरोन, आयरन सूक्ष्म पोषक तत्व और वर्मीकम्पोस्ट डालें।"],
        ["अधिक संक्रमित पेड़ों को हटाकर बाकी बाग बचाएँ।", "प्रमाणित रोग-मुक्त पौधे लगाएँ।"],
        ["फूल आने के समय छिड़काव न करें ताकि मधुमक्खियाँ सुरक्षित रहें।"],
        ["pesticides", "fertilizers", "manure"],
        ["Psyllid Control Insecticide", "Citrus Micronutrient Mix (Zn/Fe/B)", "Vermicompost & Neem Oil"],
    ),
    "Peach___Bacterial_spot": _entry(
        "Peach - Bacterial Spot",
        "Bacterial infection creating small water-soaked angular leaf spots that drop out ('shot-hole') and pit fruits.",
        ["Apply Copper-based bactericide/fungicide at dormant and early petal-fall stages (avoid high-rate copper on tender summer leaves)."],
        ["Spray bio-control Pseudomonas fluorescens.", "Apply balanced organic manure and avoid over-fertilizing with nitrogen."],
        ["Plant windbreaks to reduce wind-driven rain damage.", "Choose resistant peach varieties."],
        ["Wear goggles and gloves; avoid spraying during hot midday sun."],
        "आड़ू के बैक्टीरियल स्पॉट में पत्तियों पर छोटे धब्बे और छेद ('शॉट-होल') तथा फलों पर गड्ढे बनते हैं।",
        ["सुषुप्तावस्था और शुरुआती चरण में कॉपर आधारित जीवाणुनाशक का हल्का छिड़काव करें।"],
        ["स्यूडोमोनास फ्लोरोसेंस जैव-उपचार करें।", "संतुलित जैविक खाद दें और अधिक नाइट्रोजन से बचें।"],
        ["हवा से होने वाली बारिश की मार रोकने के लिए मेड़ पर पेड़ लगाएँ।"],
        ["तेज धूप में छिड़काव न करें और दस्ताने-चश्मा पहनें।"],
        ["pesticides", "manure"],
        ["Copper Bactericide", "Pseudomonas Bio-control", "Organic Manure"],
    ),
    "Peach___healthy": _healthy_entry("Peach", "आड़ू"),
    "Pepper,_bell___Bacterial_spot": _entry(
        "Bell Pepper - Bacterial Spot",
        "Water-soaked spots on pepper leaves turning brown-black with yellow halos, causing leaf drop and scabby fruit lesions.",
        ["Spray Copper hydroxide / Copper oxychloride + Mancozeb tank-mix group at early symptom onset."],
        ["Spray garlic-neem extract or Bacillus subtilis bio-fungicide.", "Add vermicompost and neem cake to soil."],
        ["Use disease-free seeds and drip irrigation instead of overhead sprinklers.", "Do not work in wet fields to avoid spreading bacteria."],
        ["Wear gloves and wash hands/tools after handling infected plants."],
        "शिमला मिर्च के बैक्टीरियल स्पॉट में पत्तियों पर पीले किनारे वाले काले-भूरे धब्बे बनते हैं और पत्ते झड़ते हैं।",
        ["शुरुआत में कॉपर हाइड्रॉक्साइड/ऑक्सीक्लोराइड + मैनकोजेब समूह का छिड़काव करें।"],
        ["लहसुन-नीम अर्क या बैसिलस सबटिलिस जैव-स्प्रे करें।", "मिट्टी में वर्मीकम्पोस्ट और नीम खली मिलाएँ।"],
        ["रोग-मुक्त बीज और ड्रिप सिंचाई अपनाएँ।", "गीले खेत में काम करने से बचें।"],
        ["संक्रमित पौधों को छूने के बाद हाथ और औज़ार धोएँ।"],
        ["pesticides", "manure"],
        ["Copper Hydroxide / Mancozeb", "Neem Cake & Vermicompost", "Bio-bactericide"],
    ),
    "Pepper,_bell___healthy": _healthy_entry("Bell Pepper", "शिमला मिर्च"),
    "Potato___Early_blight": _entry(
        "Potato - Early Blight",
        "Alternaria fungus creates brown concentric 'target-ring' spots on older lower leaves, lowering tuber yield.",
        ["Apply protectant Mancozeb or Chlorothalonil group fungicide; rotate with Azoxystrobin/Triazole if spreading."],
        ["Spray 2–3% neem oil weekly at initial stage.", "Apply compost and balanced potassium fertilizer to boost leaf strength."],
        ["Avoid late-evening overhead watering.", "Follow a 3-year crop rotation and clear plant debris."],
        ["Wear gloves and mask; store pesticides locked away from food grains."],
        "आलू के अर्ली ब्लाइट में पुरानी पत्तियों पर भूरे गोल छल्लेदार धब्बे बनते हैं जिससे पैदावार घटती है।",
        ["मैनकोजेब या क्लोरोथैलोनिल समूह का फफूंदनाशक छिड़कें; रोग बढ़े तो ट्रायज़ोल समूह से बदलें।"],
        ["शुरुआती अवस्था में 2–3% नीम तेल का साप्ताहिक छिड़काव करें।", "पोटाश व कम्पोस्ट खाद से पौधों की ताकत बढ़ाएँ।"],
        ["शाम को सिंचाई न करें।", "3 साल का फसल चक्र अपनाएँ और कचरा साफ करें।"],
        ["दस्ताने और मास्क पहनें; दवाइयाँ अनाज से दूर रखें।"],
        ["pesticides", "fertilizers", "manure"],
        ["Mancozeb / Chlorothalonil Fungicide", "Potash & Organic Compost", "Neem Oil"],
    ),
    "Potato___Late_blight": _entry(
        "Potato - Late Blight",
        "Aggressive water-mold (Phytophthora) causing dark water-soaked lesions with white mold under leaves in cool, humid/rainy weather.",
        ["Use systemic + contact fungicide (Metalaxyl-M + Mancozeb or Cymoxanil + Mancozeb group) strictly in dry spray windows."],
        ["Apply Trichoderma bio-protectant preventively; destroy heavily blighted haulms immediately."],
        ["Use certified blight-free seed tubers and hill up soil around stems.", "Ensure rapid field drainage."],
        ["Observe pre-harvest interval and wear full PPE."],
        "आलू का लेट ब्लाइट ठंडे व नमी वाले मौसम में तेजी से फैलता है और पत्तियों व कंदों को सड़ा देता है।",
        ["सूखे मौसम में मेटालैक्सिल+मैनकोजेब या साइमॉक्सैनिल+मैनकोजेब समूह का छिड़काव करें।"],
        ["रोकथाम के लिए ट्राइकोडर्मा का उपयोग करें; अधिक सड़े पौधे तुरंत उखाड़कर नष्ट करें।"],
        ["प्रमाणित रोग-मुक्त बीज कंद लगाएँ और मेड़ ऊंची रखें।", "खेत में पानी न जमा होने दें।"],
        ["पूर्ण सुरक्षा किट पहनें और तुड़ाई प्रतीक्षा अवधि का पालन करें।"],
        ["pesticides", "fertilizers"],
        ["Metalaxyl / Cymoxanil + Mancozeb", "Trichoderma Bio-fungicide", "Potash Fertilizer"],
    ),
    "Potato___healthy": _healthy_entry("Potato", "आलू"),
    "Raspberry___healthy": _healthy_entry("Raspberry", "रास्पबेरी"),
    "Soybean___healthy": _healthy_entry("Soybean", "सोयाबीन"),
    "Squash___Powdery_mildew": _entry(
        "Squash - Powdery Mildew",
        "White talcum-like fungal patches on upper and lower squash leaves, yellowing foliage and reducing fruit sweetness.",
        ["Apply Wettable Sulfur or Triazole/Strobilurin group fungicide on leaf undersides too."],
        ["Spray 2% neem oil or diluted buttermilk/baking-soda soap solution.", "Mulch with compost to prevent drought stress."],
        ["Space vines well for airflow and water at the soil line."],
        ["Avoid spraying sulfur above 32°C to prevent leaf burn; wear mask and gloves."],
        "कद्दू/स्क्वैश के पाउडरी मिल्ड्यू में पत्तियों पर सफेद पाउडर जैसा फफूंद फैल जाता है।",
        ["घुलनशील सल्फर या ट्रायज़ोल समूह की दवा का पत्तियों के ऊपर व नीचे छिड़काव करें।"],
        ["2% नीम तेल या छाछ/मीठा सोडा घोल का छिड़काव करें।", "कम्पोस्ट मल्चिंग से नमी बनाए रखें।"],
        ["बेलों के बीच पर्याप्त दूरी रखें और जड़ों में पानी दें।"],
        ["32°C से अधिक तापमान में सल्फर न छिड़कें; मास्क और दस्ताने पहनें।"],
        ["pesticides", "manure"],
        ["Wettable Sulfur", "Neem Oil", "Compost Manure"],
    ),
    "Strawberry___Leaf_scorch": _entry(
        "Strawberry - Leaf Scorch",
        "Fungal disease producing irregular purple-to-brown blotches that make leaf edges look scorched and dried.",
        ["Apply Captan or Strobilurin group fungicide after removing old infected foliage."],
        ["Spray neem oil or Trichoderma bio-fungicide.", "Side-dress with well-rotted compost and balanced organic nutrients."],
        ["Use drip irrigation and straw mulch to stop soil splash.", "Renovate beds after harvest."],
        ["Wear gloves and respect berry pre-harvest intervals."],
        "स्ट्रॉबेरी के लीफ स्कॉर्च में पत्तियों पर बैंगनी-भूरे धब्बे बनते हैं और किनारे जले हुए दिखते हैं।",
        ["संक्रमित पत्तियाँ हटाकर कैप्टान या स्ट्रोबिल्यूरिन समूह की दवा छिड़कें।"],
        ["नीम तेल या ट्राइकोडर्मा जैव-फफूंदनाशक उपयोग करें।", "सड़ी कम्पोस्ट खाद डालें।"],
        ["मिट्टी की छींटें रोकने के लिए पुआल मल्च और ड्रिप सिंचाई करें।"],
        ["दस्ताने पहनें और फल तोड़ने से पहले प्रतीक्षा अवधि का ध्यान रखें।"],
        ["pesticides", "manure"],
        ["Captan Fungicide", "Trichoderma / Neem Oil", "Vermicompost"],
    ),
    "Strawberry___healthy": _healthy_entry("Strawberry", "स्ट्रॉबेरी"),
    "Tomato___Bacterial_spot": _entry(
        "Tomato - Bacterial Spot",
        "Small dark water-soaked spots on leaves and raised scabby spots on fruits, spreading rapidly in warm rain.",
        ["Use Copper oxychloride / Copper hydroxide + Mancozeb group spray early."],
        ["Spray Bacillus subtilis bio-bactericide or neem-garlic extract.", "Apply vermicompost + neem cake to strengthen plants."],
        ["Stake plants, use drip irrigation, and avoid working in wet foliage."],
        ["Wear gloves and sanitize stakes/tools between seasons."],
        "टमाटर के बैक्टीरियल स्पॉट में पत्तियों पर काले धब्बे और फलों पर खुरदुरे दाग पड़ते हैं।",
        ["शुरुआत में कॉपर ऑक्सीक्लोराइड/हाइड्रॉक्साइड + मैनकोजेब समूह का छिड़काव करें।"],
        ["बैसिलस सबटिलिस या नीम-लहसुन अर्क का छिड़काव करें।", "जड़ों में वर्मीकम्पोस्ट और नीम खली डालें।"],
        ["पौधों को सहारा दें, ड्रिप सिंचाई करें और गीले पौधों को न छुएँ।"],
        ["दस्ताने पहनें और औज़ारों को साफ रखें।"],
        ["pesticides", "manure"],
        ["Copper Oxychloride + Mancozeb", "Neem Cake & Vermicompost", "Bio-bactericide"],
    ),
    "Tomato___Early_blight": _entry(
        "Tomato - Early Blight",
        "Brown concentric target-like rings on older tomato leaves that yellow and drop, exposing fruit to sunscald.",
        ["Apply Mancozeb or Chlorothalonil group fungicide; rotate with Azoxystrobin/Difenoconazole if needed."],
        ["Spray 2% neem oil or compost tea.", "Enrich soil with vermicompost and potash."],
        ["Remove lower leaves touching soil, mulch beds, and avoid evening overhead watering."],
        ["Wear PPE and wash hands after handling foliage."],
        "टमाटर के अर्ली ब्लाइट में निचली पत्तियों पर भूरे छल्लेदार धब्बे बनते हैं और पत्ते पीले होकर झड़ते हैं।",
        ["मैनकोजेब या क्लोरोथैलोनिल समूह का छिड़काव करें; जरूरत पर स्ट्रोबिल्यूरिन/ट्रायज़ोल से बदलें।"],
        ["2% नीम तेल या कम्पोस्ट टी छिड़कें।", "मिट्टी में वर्मीकम्पोस्ट और पोटाश मिलाएँ।"],
        ["जमीन छूने वाली निचली पत्तियाँ हटाएँ और मल्चिंग करें।"],
        ["सुरक्षा किट पहनें और काम के बाद हाथ धोएँ।"],
        ["pesticides", "fertilizers", "manure"],
        ["Mancozeb / Chlorothalonil", "Vermicompost & Potash", "Neem Oil"],
    ),
    "Tomato___Late_blight": _entry(
        "Tomato - Late Blight",
        "Fast-spreading water-mold causing dark greasy leaf blotches, white mold undersides, and firm brown fruit rot in humid/rainy weather.",
        ["Use systemic+contact fungicide (Cymoxanil+Mancozeb or Dimethomorph+Mancozeb group) only in rain-free windows."],
        ["Remove and bag/destroy infected leaves immediately.", "Preventive 2% neem oil or Trichoderma spray on healthy neighbors."],
        ["Increase plant spacing, stake vines, and ensure good drainage."],
        ["Wear mask and gloves; follow pre-harvest intervals strictly."],
        "टमाटर का लेट ब्लाइट नमी व बारिश में बहुत तेजी से पत्तियों और फलों को काला कर सड़ा देता है।",
        ["बारिश रुकने पर साइमॉक्सैनिल+मैनकोजेब या डाईमेथोमॉर्फ+मैनकोजेब समूह की दवा छिड़कें।"],
        ["संक्रमित पत्तियाँ तुरंत तोड़कर नष्ट करें।", "स्वस्थ पौधों पर नीम तेल या ट्राइकोडर्मा छिड़कें।"],
        ["पौधों के बीच दूरी रखें, सहारा दें और जल निकासी सही रखें।"],
        ["मास्क और दस्ताने पहनें तथा तुड़ाई प्रतीक्षा अवधि का पालन करें।"],
        ["pesticides", "fertilizers"],
        ["Cymoxanil / Dimethomorph + Mancozeb", "Trichoderma Bio-fungicide", "Neem Oil"],
    ),
    "Tomato___Leaf_Mold": _entry(
        "Tomato - Leaf Mold",
        "Yellow upper-leaf blotches with olive-green velvety mold underneath, thriving in high humidity and polyhouses.",
        ["Apply Copper or Chlorothalonil/Strobilurin group fungicide targeting leaf undersides."],
        ["Prune lower leaves and apply baking-soda + mild soap or neem spray.", "Add balanced organic compost."],
        ["Ventilate greenhouses/polyhouses and avoid wetting leaves."],
        ["Avoid inhaling mold spores or spray mist; wear mask."],
        "लीफ मोल्ड में पत्तियों के ऊपर पीले धब्बे और नीचे जैतून रंग की मखमली फफूंद दिखती है।",
        ["पत्तियों के निचले हिस्से पर कॉपर या क्लोरोथैलोनिल समूह की दवा छिड़कें।"],
        ["निचली पत्तियाँ काटें और नीम तेल या बेकिंग सोडा घोल छिड़कें।", "संतुलित जैविक खाद दें।"],
        ["पॉलीहाउस में हवा का प्रवाह बढ़ाएँ और पत्तियाँ गीली न होने दें।"],
        ["स्प्रे की धुंध सांस में न लें; मास्क पहनें।"],
        ["pesticides", "manure"],
        ["Copper / Chlorothalonil Fungicide", "Neem Oil", "Organic Compost"],
    ),
    "Tomato___Septoria_leaf_spot": _entry(
        "Tomato - Septoria Leaf Spot",
        "Numerous small circular spots with dark margins and gray centers on lower leaves after rain splash.",
        ["Spray Mancozeb or Chlorothalonil group fungicide at 7–10 day intervals."],
        ["Remove spotted lower leaves and spray 2% neem oil or copper soap.", "Mulch around base with dry straw or compost."],
        ["Do not overhead-irrigate; stake plants and rotate away from solanaceous crops."],
        ["Wear gloves and clean tools after pruning."],
        "सेप्टोरिया लीफ स्पॉट में निचली पत्तियों पर बीच से स्लेटी और किनारे से गहरे छोटे गोल धब्बे बनते हैं।",
        ["मैनकोजेब या क्लोरोथैलोनिल समूह का 7–10 दिन के अंतर पर छिड़काव करें।"],
        ["धब्बेदार निचली पत्तियाँ हटाएँ और नीम तेल छिड़कें।", "पौधे के नीचे पुआल या कम्पोस्ट से मल्चिंग करें।"],
        ["ऊपर से पानी न दें और फसल चक्र अपनाएँ।"],
        ["दस्ताने पहनें और छंटाई के औज़ार साफ करें।"],
        ["pesticides", "manure"],
        ["Mancozeb / Chlorothalonil", "Neem Oil", "Compost / Mulch"],
    ),
    "Tomato___Spider_mites Two-spotted_spider_mite": _entry(
        "Tomato - Two-Spotted Spider Mite",
        "Tiny sap-sucking mites causing yellow stippling, bronzed leaves, and fine webbing in hot, dry weather.",
        ["Use a specific Miticide/Acaricide group (Abamectin or Spiromesifen or Wettable Sulfur) — standard insecticides worsen mites."],
        ["Spray 2% neem oil or horticultural soap thoroughly on leaf undersides.", "Mist plants with water to reduce dust and dry heat stress; apply compost."],
        ["Control weeds around field borders and avoid dusty conditions."],
        ["Rotate miticide groups to prevent resistance; wear mask and gloves."],
        "स्पाइडर माइट पत्तियों का रस चूसकर पीले बिंदु, तांबे जैसा रंग और बारीक जाला बनाती है।",
        ["केवल माइटनाशी समूह (एबामेक्टिन/स्पाइरोमेसिफेन या घुलनशील सल्फर) उपयोग करें — सामान्य कीटनाशक से माइट बढ़ते हैं।"],
        ["पत्तियों के नीचे 2% नीम तेल या कीटनाशक साबुन का छिड़काव करें।", "सूखे व धूल वाले मौसम में हल्की नमी और कम्पोस्ट दें।"],
        ["खेत की मेड़ से खरपतवार हटाएँ।"],
        ["दवा समूह बदलते रहें और मास्क-दस्ताने पहनें।"],
        ["pesticides", "manure"],
        ["Miticide (Abamectin / Wettable Sulfur)", "Neem Oil", "Organic Compost"],
    ),
    "Tomato___Target_Spot": _entry(
        "Tomato - Target Spot",
        "Dark necrotic spots with concentric rings on leaves, stems, and fruits in warm humid climates.",
        ["Apply Chlorothalonil, Mancozeb, or Strobilurin group fungicide."],
        ["Prune lower foliage, spray neem oil or Trichoderma bio-fungicide, and enrich soil with vermicompost."],
        ["Improve spacing and air circulation; remove crop debris after harvest."],
        ["Wear PPE and follow safe harvest intervals."],
        "टारगेट स्पॉट में पत्तियों, तनों और फलों पर छल्लेदार गहरे धब्बे बनते हैं।",
        ["क्लोरोथैलोनिल, मैनकोजेब या स्ट्रोबिल्यूरिन समूह के फफूंदनाशक का उपयोग करें।"],
        ["निचली पत्तियाँ काटें, नीम तेल या ट्राइकोडर्मा छिड़कें और वर्मीकम्पोस्ट डालें।"],
        ["पौधों के बीच हवा का प्रवाह रखें और कटाई के बाद अवशेष हटाएँ।"],
        ["सुरक्षा किट पहनें और तुड़ाई प्रतीक्षा अवधि मानें।"],
        ["pesticides", "manure"],
        ["Chlorothalonil / Mancozeb", "Trichoderma Bio-fungicide", "Vermicompost"],
    ),
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": _entry(
        "Tomato - Yellow Leaf Curl Virus (TYLCV)",
        "Viral disease transmitted by whiteflies causing upward leaf curling, yellowing margins, and stunted growth. Cannot be cured with fungicides.",
        ["Control whitefly vectors using Imidacloprid / Thiamethoxam / Pyriproxyfen group rotation (no fungicide works on viruses)."],
        ["Install yellow sticky traps and spray 2% neem oil + garlic-chili extract for whiteflies.", "Support plant vigor with humic acid and vermicompost."],
        ["Uproot and bury early infected plants; use insect-proof nursery nets and resistant seeds."],
        ["Protect pollinators by avoiding sprays during peak bee foraging hours."],
        "लीफ कर्ल वायरस सफेद मक्खी से फैलता है जिससे पत्तियाँ ऊपर मुड़कर पीली पड़ती हैं और पौधा बौना रह जाता है।",
        ["फफूंदनाशक वायरस पर काम नहीं करते; सफेद मक्खी रोकने हेतु इमिडाक्लोप्रिड/थायोमेथोक्साम/पाइरीप्रॉक्सीफेन समूह बदलकर छिड़कें।"],
        ["खेत में पीले चिपचिपे कार्ड (Yellow Sticky Traps) लगाएँ और 2% नीम तेल छिड़कें।", "वर्मीकम्पोस्ट व ह्यूमिक खाद दें।"],
        ["शुरुआती संक्रमित पौधों को उखाड़कर दबा दें और प्रतिरोधी बीज लगाएँ।"],
        ["मधुमक्खियों के समय छिड़काव से बचें और सुरक्षा किट पहनें।"],
        ["pesticides", "manure", "fertilizers"],
        ["Yellow Sticky Traps", "Whitefly Insecticide", "Neem Oil & Vermicompost"],
    ),
    "Tomato___Tomato_mosaic_virus": _entry(
        "Tomato - Tomato Mosaic Virus",
        "Highly contagious contact virus causing light/dark green mottling and fern-like leaf distortion. No chemical cure exists.",
        ["No chemical spray cures viruses; focus on sanitation and sucking-pest control if aphids/thrips are present."],
        ["Spray diluted skim milk (1:9 water) on tools/hands to inactivate virus contact.", "Strengthen healthy plants with vermicompost and balanced micronutrients."],
        ["Remove infected plants gently without brushing healthy ones; wash hands with soap before touching crops (avoid tobacco near plants)."],
        ["Disinfect pruning shears in milk or 10% trisodium phosphate solution."],
        "मोज़ेक वायरस छूने से तेजी से फैलता है और पत्तियों पर हल्के-गहरे हरे चितकबरे धब्बे बनाता है।",
        ["किसी भी रासायनिक स्प्रे से वायरस ठीक नहीं होता; केवल रस चूसने वाले कीट दिखें तो नियंत्रण करें।"],
        ["औज़ारों व हाथों को दूध के घोल (1:9) या साबुन से साफ करें।", "स्वस्थ पौधों को वर्मीकम्पोस्ट व सूक्ष्म पोषक तत्व दें।"],
        ["संक्रमित पौधे सावधानी से हटाएँ और पौधों के पास तंबाकू का उपयोग न करें।"],
        ["कटाई के औज़ारों को हर पौधे के बाद कीटाणुरहित करें।"],
        ["manure", "fertilizers"],
        ["Vermicompost & Micronutrients", "Neem Oil (Vector Prevention)", "Sanitizing Soap / Bio-enhancer"],
    ),
    "Tomato___healthy": _healthy_entry("Tomato", "टमाटर"),
}

DEFAULT_INFO: Dict[str, Any] = _entry(
    "Plant Diagnosis Advisory",
    "Specific disease entry not matched; follow general integrated pest & nutrient management.",
    ["Consult a local agricultural officer or Krishi Vigyan Kendra before applying chemical pesticides."],
    ["Remove visibly damaged leaves and spray 2% neem oil preventively.", "Apply well-rotted compost or vermicompost."],
    ["Ensure good drainage, airflow, and crop rotation."],
    ["Always wear gloves and a mask during any spray operation."],
    "इस रोग के लिए सामान्य एकीकृत फसल सुरक्षा सलाह का पालन करें।",
    ["रासायनिक दवा डालने से पहले नजदीकी कृषि विज्ञान केंद्र या विशेषज्ञ की सलाह लें।"],
    ["रोगग्रस्त पत्तियाँ हटाएँ और रोकथाम के लिए 2% नीम तेल का छिड़काव करें।", "सड़ी हुई जैविक खाद या वर्मीकम्पोस्ट डालें।"],
    ["जल निकासी, हवा का प्रवाह और फसल चक्र बनाए रखें।"],
    ["छिड़काव के समय हमेशा मास्क और दस्ताने पहनें।"],
    ["pesticides", "manure", "fertilizers"],
    ["Neem Oil", "Vermicompost", "Balanced NPK Fertilizer"],
)


def get_local_recommendation(
    class_name: str,
    soil_pH: Optional[float] = None,
    spray_count: int = 0,
    weather_summary: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Return weather-, soil-, and spray-aware structured bilingual advice offline."""
    base = DISEASE_INFO.get(class_name, DEFAULT_INFO)
    is_healthy = "___healthy" in class_name

    en = {k: list(v) if isinstance(v, list) else v for k, v in base["english"].items()}
    hi = {k: list(v) if isinstance(v, list) else v for k, v in base["hindi"].items()}
    categories = list(base["store_categories"])
    shopping = list(base["shopping_items"])

    weather_summary = weather_summary or {}
    humidity = weather_summary.get("avg_humidity")
    rain = weather_summary.get("total_rain_mm")

    if not is_healthy and ((humidity is not None and humidity > 80) or (rain is not None and rain > 5)):
        en["chemical"].insert(0, "Weather Alert: High humidity/rain forecasted — wait for a 6+ hour dry window before spraying so chemicals do not wash off.")
        hi["chemical"].insert(0, "मौसम चेतावनी: अधिक नमी या बारिश की संभावना है — दवा बहने से बचाने के लिए कम से कम 6 घंटे सूखे मौसम का इंतजार करें।")

    if soil_pH is not None and soil_pH > 0:
        if soil_pH < 5.5:
            en["prevention"].append(f"Soil pH is acidic ({soil_pH}). Apply agricultural lime (dolomite) and organic compost to raise pH.")
            hi["prevention"].append(f"मिट्टी अम्लीय (pH {soil_pH}) है। सुधार के लिए कृषि चूना (डोलोमाइट) और जैविक खाद डालें।")
            if "fertilizers" not in categories:
                categories.append("fertilizers")
            shopping.append("Agricultural Lime (pH Corrector)")
        elif soil_pH > 7.5:
            en["prevention"].append(f"Soil pH is alkaline ({soil_pH}). Apply elemental sulfur, gypsum, or acidic organic compost/manure.")
            hi["prevention"].append(f"मिट्टी क्षारीय (pH {soil_pH}) है। सुधार के लिए गंधक (सल्फर), जिप्सम या सड़ी जैविक खाद डालें।")
            if "fertilizers" not in categories:
                categories.append("fertilizers")
            shopping.append("Agricultural Sulfur / Gypsum")

    if not is_healthy and spray_count >= 3:
        en["safety"].insert(0, f"Resistance Warning: {spray_count} chemical sprays already used this season — switch to a different chemical group (FRAC/IRAC) or organic bio-control.")
        hi["safety"].insert(0, f"चेतावनी: इस मौसम में {spray_count} रासायनिक छिड़काव हो चुके हैं — प्रतिरोध से बचने के लिए दवा का समूह बदलें या जैविक उपाय अपनाएँ।")

    return {
        "friendly_name": base["friendly_name"],
        "store_categories": categories,
        "shopping_items": shopping,
        "english": en,
        "hindi": hi,
    }


def format_advice_text(structured: Dict[str, Any]) -> str:
    """Format structured advice into readable EN + HI text for backwards compatibility."""
    en = structured["english"]
    hi = structured["hindi"]
    en_block = (
        f"[ENGLISH]\n"
        f"1. Disease Summary: {en['summary']}\n"
        f"2. Chemical Control: {'; '.join(en['chemical'])}\n"
        f"3. Organic / Manure Options: {'; '.join(en['organic'])}\n"
        f"4. Soil & Preventive Care: {'; '.join(en['prevention'])}\n"
        f"5. Safety Precautions: {'; '.join(en['safety'])}\n"
    )
    hi_block = (
        f"\n[HINDI]\n"
        f"1. रोग सारांश: {hi['summary']}\n"
        f"2. रासायनिक उपचार: {'; '.join(hi['chemical'])}\n"
        f"3. जैविक / खाद उपचार: {'; '.join(hi['organic'])}\n"
        f"4. मिट्टी व रोकथाम उपाय: {'; '.join(hi['prevention'])}\n"
        f"5. सुरक्षा सावधानियाँ: {'; '.join(hi['safety'])}\n"
    )
    return en_block + hi_block
