# Extended offline backup treatment knowledge base
# (Used when Gemini API fails or internet unavailable)

DISEASE_INFO = {

    ### TOMATO LATE BLIGHT ###
    "Tomato___Late_blight": {
        "friendly_name": "Tomato - Late blight",
        "english": {
            "summary": "Late blight is a severe fungal disease causing dark lesions on leaves and fruit, rapidly spreading in humid weather.",
            "chemical": [
                "Use protectant fungicide from Mancozeb or Chlorothalonil group.",
                "Avoid spraying right before rain to prevent wash-off."
            ],
            "organic": [
                "Remove infected leaves and dispose away from field.",
                "Spray 2% neem oil weekly at early stage."
            ],
            "prevention": [
                "Maintain airflow, avoid overcrowding.",
                "Perform crop rotation every 2–3 years."
            ],
            "safety": [
                "Wear gloves and mask while spraying.",
                "Follow pre-harvest interval after chemical spray."
            ]
        },
        "hindi": {
            "summary": "लेट ब्लाइट टमाटर की पत्तियों और फलों पर काले धब्बे बनाकर तेजी से फैलने वाला रोग है।",
            "chemical": [
                "मैनकोजेब या क्लोरोथैलोनिल समूह की दवा उपयोग करें।",
                "बारिश से ठीक पहले दवा का छिड़काव न करें।"
            ],
            "organic": [
                "संक्रमित पत्तियों को तोड़कर नष्ट कर दें।",
                "शुरुआती अवस्था में 2% नीम तेल छिड़कें।"
            ],
            "prevention": [
                "उचित दूरी रखें और हवा का प्रवाह बनाए रखें।",
                "हर 2-3 साल में फसल चक्र अपनाएँ।"
            ],
            "safety": [
                "छिड़काव करते समय मास्क और दस्ताने पहनें।",
                "फसल तोड़ने से पहले प्रतीक्षा अवधि का पालन करें।"
            ]
        }
    },

    ### TOMATO EARLY BLIGHT ###
    "Tomato___Early_blight": {
        "friendly_name": "Tomato - Early blight",
        "english": {
            "summary": "Early blight creates brown concentric rings on older leaves, reducing plant vigor and fruiting.",
            "chemical": [
                "Use fungicides from Mancozeb or Copper oxychloride group.",
                "Spray at 7–10 day intervals during wet season."
            ],
            "organic": [
                "Use compost tea / cow dung slurry foliar spray.",
                "Improve soil health with organic matter."
            ],
            "prevention": [
                "Do not overhead irrigate late evening.",
                "Remove plant debris after harvest."
            ],
            "safety": [
                "Store pesticide bottles in cool dry place.",
                "Do not allow spray to drift toward animals."
            ]
        },
        "hindi": {
            "summary": "अर्ली ब्लाइट पत्तियों पर भूरे गोलाकार निशान बनाता है जिससे पौधे कमजोर हो जाते हैं।",
            "chemical": [
                "मैनकोजेब या कॉपर ऑक्सीक्लोराइड समूह की दवाइयाँ उपयोग करें।",
                "गर्म और गीले मौसम में 7-10 दिनों पर छिड़काव।"
            ],
            "organic": [
                "कम्पोस्ट टी या गोबर घोल का छिड़काव करें।",
                "मिट्टी में जैविक खाद मिलाएँ।"
            ],
            "prevention": [
                "शाम को पानी न दें।",
                "फसल कटाई के बाद अवशेष हटाएँ।"
            ],
            "safety": [
                "दवाइयाँ बच्चों की पहुँच से दूर रखें।",
                "छिड़काव के दौरान पशुओं को दूर रखें।"
            ]
        }
    },

    ### TOMATO LEAF MOLD ###
    "Tomato___Leaf_Mold": {
        "friendly_name": "Tomato - Leaf Mold",
        "english": {
            "summary": "Leaf mold appears as yellow spots on top of leaf with olive-colored mold under the leaf.",
            "chemical": [
                "Use spray from Copper group fungicides.",
                "Improve ventilation in polyhouse."
            ],
            "organic": [
                "Reduce shade and humidity.",
                "Apply baking soda + soap solution (small scale)."
            ],
            "prevention": [
                "Do not wet leaves during watering.",
                "Prune lower leaves regularly."
            ],
            "safety": [
                "Avoid inhaling spray mist.",
                "Wash hands after handling plants."
            ]
        },
        "hindi": {
            "summary": "लीफ मोल्ड में पत्ते के ऊपर पीले धब्बे और नीचे जैतून रंग की फफूंद दिखती है।",
            "chemical": [
                "कॉपर आधारित फफूंदनाशक उपयोग करें।",
                "ग्रीनहाउस में हवा का प्रवाह बढ़ाएँ।"
            ],
            "organic": [
                "छाया और नमी कम करें।",
                "बेकिंग सोडा घोल का छिड़काव (छोटे स्तर पर)।"
            ],
            "prevention": [
                "पत्तियों को गीला न होने दें।",
                "निचली पत्तियाँ समय-समय पर काटें।"
            ],
            "safety": [
                "स्प्रे मिस्ट को सांस में न लें।",
                "छूने के बाद हाथ धोएँ।"
            ]
        }
    },

    ### APPLE BLACK ROT ###
    "Apple___Black_rot": {
        "friendly_name": "Apple - Black Rot",
        "english": {
            "summary": "Black Rot affects fruit, leaves and bark causing black lesions and fruit rot.",
            "chemical": [
                "Use Copper oxychloride based fungicides before infection spreads.",
                "Remove mummified fruits from the tree."
            ],
            "organic": [
                "Prune infected branches.",
                "Use cow urine + neem mix spray."
            ],
            "prevention": [
                "Proper pruning to reduce humidity.",
                "Disinfect pruning tools."
            ],
            "safety": [
                "Wear glasses and gloves.",
                "Do not burn plastic mixed plant waste."
            ]
        },
        "hindi": {
            "summary": "ब्लैक रॉट से पत्तियों और फलों पर काले धब्बे बनते हैं और फल सड़ जाते हैं।",
            "chemical": [
                "कॉपर समूह की फफूंदनाशक दवा का प्रयोग।",
                "सूखे सड़े हुए फलों को हटाएँ।"
            ],
            "organic": [
                "संक्रमित टहनियाँ काटें।",
                "गोमूत्र + नीम मिश्रण छिड़कें।"
            ],
            "prevention": [
                "छंटाई करें और नमी कम रखें।",
                "छंटाई वाले औज़ारों को सैनिटाइज करें।"
            ],
            "safety": [
                "चश्मा और दस्ताने पहनें।",
                "प्लास्टिक मिले पौधों के कचरे को न जलाएँ।"
            ]
        }
    },

    ### APPLE CEDAR RUST ###
    "Apple___Cedar_apple_rust": {
        "friendly_name": "Apple - Cedar Apple Rust",
        "english": {
            "summary": "This disease causes bright orange spots on leaves due to fungal spores spread by juniper trees.",
            "chemical": [
                "Use fungicide spray from Copper or Mancozeb group."
            ],
            "organic": [
                "Remove nearby juniper bushes.",
                "Mix turmeric and cow dung paste on small infections."
            ],
            "prevention": [
                "Grow resistant apple varieties.",
                "Avoid planting near juniper."
            ],
            "safety": [
                "Wear mask while spraying.",
                "Do not contaminate water sources."
            ]
        },
        "hindi": {
            "summary": "यह रोग पत्तों पर नारंगी धब्बे बनाता है और जूनीपर पेड़ से फैलता है।",
            "chemical": [
                "कॉपर या मैनकोजेब समूह की दवा उपयोग करें।"
            ],
            "organic": [
                "पास के जूनीपर पौधे हटाएँ।",
                "हल्का संक्रमण हो तो हल्दी + गोबर लगाएँ।"
            ],
            "prevention": [
                "प्रतिरोधी किस्में लगाएँ।",
                "जूनीपर के पास बाग़ न लगाएँ।"
            ],
            "safety": [
                "स्प्रे करते समय मास्क पहनें।",
                "दवा को पानी में न मिलाएँ।"
            ]
        }
    },

    ### GRAPE BLACK ROT ###
    "Grape___Black_rot": {
        "friendly_name": "Grape - Black Rot",
        "english": {
            "summary": "Black rot causes dark spots on leaves and dries grape berries into black mummies.",
            "chemical": [
                "Spray with Copper-based fungicides.",
                "Start spray when new leaves emerge."
            ],
            "organic": [
                "Remove infected grapes immediately.",
                "Use wood ash / neem solution."
            ],
            "prevention": [
                "Support vines to improve airflow.",
                "Do not irrigate late evening."
            ],
            "safety": [
                "Wear rubber gloves.",
                "Wash sprayer after use."
            ]
        },
        "hindi": {
            "summary": "ग्रेप ब्लैक रॉट में पत्तियाँ और फल काले होकर सूख जाते हैं।",
            "chemical": [
                "कॉपर आधारित दवा का छिड़काव करें।",
                "नई पत्तियों के आने पर स्प्रे शुरू करें।"
            ],
            "organic": [
                "संक्रमित अंगूर तुरंत हटाएँ।",
                "नीम घोल/राख का उपयोग।"
            ],
            "prevention": [
                "बेलों को सहारा दें और हवा का रास्ता बनाएं।",
                "शाम में सिंचाई न करें।"
            ],
            "safety": [
                "रबर के दस्ताने पहनें।",
                "स्प्रेयर को इस्तेमाल के बाद धोएँ।"
            ]
        }
    },

    ### CORN COMMON RUST ###
    "Corn___Common_rust": {
        "friendly_name": "Corn - Common Rust",
        "english": {
            "summary": "Rust causes reddish-brown pustules on leaves affecting plant growth.",
            "chemical": [
                "Use fungicide from Triazole group if severe."
            ],
            "organic": [
                "Increase spacing for better airflow.",
                "Use neem-based foliar spray."
            ],
            "prevention": [
                "Use rust-resistant varieties.",
                "Avoid excessive nitrogen fertilization."
            ],
            "safety": [
                "Spray upwind direction.",
                "Keep animals away from sprayed plots."
            ]
        },
        "hindi": {
            "summary": "कॉर्न रस्ट में पत्तियों पर भूरे रंग के उभार बनते हैं।",
            "chemical": [
                "आवश्यक हो तो ट्रायज़ोल समूह की दवा स्प्रे करें।"
            ],
            "organic": [
                "पौधों के बीच दूरी रखें।",
                "नीम आधारित छिड़काव करें।"
            ],
            "prevention": [
                "प्रतिरोधी किस्मों का चयन करें।",
                "अत्यधिक नाइट्रोजन उर्वरक न डालें।"
            ],
            "safety": [
                "हवा की दिशा देखकर ही स्प्रे करें।",
                "छिड़काव के बाद पशु दूर रखें।"
            ]
        }
    },
        ### POTATO EARLY BLIGHT ###
    "Potato___Early_blight": {
        "friendly_name": "Potato - Early blight",
        "english": {
            "summary": "Early Blight causes brown concentric ring lesions on older leaves, reducing tuber size and yield.",
            "chemical": [
                "Use protectant fungicide from Chlorothalonil or Mancozeb group.",
                "If disease progresses, use systemic fungicide from Triazole group (dose as per label)."
            ],
            "organic": [
                "Spray 2–3% neem oil weekly at initial stage.",
                "Apply compost and maintain soil fertility to improve disease resistance."
            ],
            "prevention": [
                "Avoid overhead irrigation late evening.",
                "Remove plant debris and follow a 3-year crop rotation.",
                "Provide wider spacing for airflow."
            ],
            "safety": [
                "Wear gloves and avoid inhaling mist during spray.",
                "Store chemicals locked and away from food grains."
            ]
        },
        "hindi": {
            "summary": "अर्ली ब्लाइट में पुरानी पत्तियों पर भूरे गोलाकार धब्बे बनते हैं जिससे उत्पादन कम हो जाता है।",
            "chemical": [
                "क्लोरोथैलोनिल या मैनकोजेब समूह की दवा से छिड़काव करें।",
                "यदि रोग बढ़े तो ट्रायज़ोल समूह की प्रणालीगत दवा का उपयोग करें (लेबल के अनुसार मात्रा)।"
            ],
            "organic": [
                "शुरुआत में 2–3% नीम तेल का छिड़काव करें।",
                "मिट्टी की उर्वरता बढ़ाने के लिए कम्पोस्ट मिलाएँ।"
            ],
            "prevention": [
                "शाम में पानी न दें।",
                "खेत की सफाई करें और फसल चक्र अपनाएँ।",
                "हवा का प्रवाह सुनिश्चित करें।"
            ],
            "safety": [
                "छिड़काव के समय दस्ताने पहनें।",
                "दवाइयों को अनाज के पास न रखें।"
            ]
        }
    },

}

# Default fallback if disease name not found
DEFAULT_INFO = {
    "friendly_name": "Unknown disease (local backup advice)",
    "english": {
        "summary": "Disease not available in local database.",
        "chemical": [
            "Consult agricultural expert for chemical options."
        ],
        "organic": [
            "Maintain field hygiene.",
            "Use neem-based general sprays."
        ],
        "prevention": [
            "Use quality seeds and crop rotation.",
            "Avoid waterlogging."
        ],
        "safety": [
            "Wear protective gear while spraying.",
            "Do not dispose chemicals in open water."
        ]
    },
    "hindi": {
        "summary": "यह रोग स्थानीय डाटा में उपलब्ध नहीं है।",
        "chemical": [
            "कृषि विशेषज्ञ से सलाह लें।"
        ],
        "organic": [
            "खेत की सफाई रखें।",
            "नीम आधारित छिड़काव करें।"
        ],
        "prevention": [
            "स्वस्थ बीज और फसल चक्र अपनाएँ।",
            "खेत में पानी न भरने दें।"
        ],
        "safety": [
            "छिड़काव के समय सुरक्षा किट पहनें।",
            "दवाइयों को जल स्रोत में न फेंकें।"
        ]
    }

}

def get_local_recommendation(class_name):
    return DISEASE_INFO.get(class_name, DEFAULT_INFO)
