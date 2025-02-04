from transformers import BertTokenizer, BertModel
import torch
import numpy as np

class BERTChatbot:
    def __init__(self):
        try:
            self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
            self.model = BertModel.from_pretrained('bert-base-uncased')
        except Exception as e:
            print(f"Model yüklenirken hata oluştu: {str(e)}")
            raise
        
    def process_message(self, message):
        try:
            # Mesajı tokenize et
            inputs = self.tokenizer(message, return_tensors="pt", padding=True, truncation=True)
            
            # BERT modelinden çıktı al
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            # Mesajı analiz et
            message_lower = message.lower()
            
            if "cari kart" in message_lower and "ekle" in message_lower:
                return "Cari kart ekleme işlemi başlatılıyor..."
            elif "cari kart" in message_lower and "sil" in message_lower:
                return "Cari kart silme işlemi başlatılıyor..."
            elif "cari kart" in message_lower and "güncelle" in message_lower:
                return "Cari kart güncelleme işlemi başlatılıyor..."
            elif "cari kart" in message_lower and "listele" in message_lower:
                return "Cari kartlar listeleniyor..."
            else:
                return "Üzgünüm, bu işlemi anlayamadım. Lütfen 'cari kart ekle', 'cari kart sil', 'cari kart güncelle' veya 'cari kart listele' şeklinde bir komut girin."
                
        except Exception as e:
            return f"İşlem sırasında bir hata oluştu: {str(e)}"