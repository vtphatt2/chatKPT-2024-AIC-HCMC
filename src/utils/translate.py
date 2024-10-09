from deep_translator import GoogleTranslator

# Your text in Vietnamese
vietnamese_text = "bạn cảm thấy như thế nào?"

# Translate the text from Vietnamese to English
translated_text = GoogleTranslator(source='vi', target='en').translate(vietnamese_text)

# Print the translated text
print("Translated Text:", translated_text)
