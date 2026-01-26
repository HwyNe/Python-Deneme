import json
import os
from datetime import datetime

# ANSI Renk Kodları
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class Task:
    def __init__(self, name, priority="Orta", category="Genel", status="Bekliyor", created_at=None):
        self.name = name
        self.priority = priority
        self.category = category
        self.status = status
        self.created_at = created_at if created_at else datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

class TaskManager:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [Task.from_dict(t) for t in data]
        except:
            return []

    def save_tasks(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4, ensure_ascii=False)

    def show_tasks(self):
        if not self.tasks:
            print(f"\n{Colors.WARNING}📭 Liste boş.{Colors.ENDC}")
            return
        
        print(f"\n{Colors.HEADER}{'NO':<4} {'GÖREV ADI':<25} {'ÖNCELİK':<10} {'DURUM'}{Colors.ENDC}")
        print("-" * 55)
        for i, t in enumerate(self.tasks, 1):
            s_color = Colors.GREEN if t.status == "Tamamlandı" else Colors.WARNING
            print(f"{i:<4} {t.name:<25} {t.priority:<10} {s_color}{t.status}{Colors.ENDC}")

    def complete_task(self, index):
        try:
            task = self.tasks[index - 1]
            task.status = "Tamamlandı"
            self.save_tasks()
            print(f"\n{Colors.GREEN}🎉  Harika! '{task.name}' görevi tamamlandı olarak işaretlendi.{Colors.ENDC}")
        except IndexError:
            print(f"\n{Colors.FAIL}❌  Geçersiz görev numarası.{Colors.ENDC}")

    def delete_task(self, index):
        try:
            removed = self.tasks.pop(index - 1)
            self.save_tasks()
            print(f"\n{Colors.FAIL}🗑️  Silindi: {removed.name}{Colors.ENDC}")
        except IndexError:
            print(f"\n{Colors.FAIL}❌  Geçersiz görev numarası.{Colors.ENDC}")

def get_valid_input(prompt, options=None):
    while True:
        value = input(prompt).strip()
        if not value:
            print(f"{Colors.FAIL}Boş bırakılamaz.{Colors.ENDC}")
            continue
        if options and value not in options:
            print(f"{Colors.FAIL}Lütfen şunlardan birini seçin: {', '.join(options)}{Colors.ENDC}")
            continue
        return value

def main():
    manager = TaskManager()
    
    while True:
        print(f"\n{Colors.BOLD}{Colors.CYAN}--- 📝 YENİLİKÇİ GÖREV YÖNETİCİSİ ---{Colors.ENDC}")
        print("1. 📋 Görevleri Listele")
        print("2. ➕ Yeni Görev Ekle")
        print("3. ✅ Görevi Tamamla")
        print("4. 🗑️  Görevi Sil")
        print("5. 🚪 Çıkış")
        
        choice = input(f"\n{Colors.BOLD}Seçiminiz (1-5): {Colors.ENDC}")

        if choice == '1':
            manager.show_tasks()
        elif choice == '2':
            name = get_valid_input("Görev adı: ")
            print("Öncelik Seçenekleri: (1) Yüksek, (2) Orta, (3) Düşük")
            p_choice = get_valid_input("Öncelik seçin (1-3): ", ['1', '2', '3'])
            priority_map = {'1': 'Yüksek', '2': 'Orta', '3': 'Düşük'}
            
            category = input("Kategori (Opsiyonel, varsayılan 'Genel'): ").strip() or "Genel"
            
            manager.add_task(name, priority_map[p_choice], category)
            
        elif choice == '3':
            manager.show_tasks()
            if manager.tasks:
                try:
                    idx = int(input("Tamamlanacak görev numarası: "))
                    manager.complete_task(idx)
                except ValueError:
                     print(f"\n{Colors.FAIL}❌  Lütfen geçerli bir sayı girin.{Colors.ENDC}")

        elif choice == '4':
            manager.show_tasks()
            if manager.tasks:
                try:
                    idx = int(input("Silinecek görev numarası: "))
                    manager.delete_task(idx)
                except ValueError:
                    print(f"\n{Colors.FAIL}❌  Lütfen geçerli bir sayı girin.{Colors.ENDC}")

        elif choice == '5':
            print(f"\n{Colors.CYAN}Güle güle! 👋 İyi çalışmalar.{Colors.ENDC}")
            break
        else:
            print(f"\n{Colors.FAIL}❌  Geçersiz seçim, lütfen tekrar deneyin.{Colors.ENDC}")

if __name__ == "__main__":
    main()