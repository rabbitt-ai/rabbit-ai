def extract_entity(text):
    """
    Metinden önemli bilgileri çıkaran yardımcı fonksiyon
    """
    entities = {
        'isim': None,
        'işlem': None,
    }
    
    # Basit bir örnek implementasyon
    words = text.lower().split()
    if "isimde" in words:
        idx = words.index("isimde")
        if idx > 0:
            entities['isim'] = words[idx-1]
    
    return entities