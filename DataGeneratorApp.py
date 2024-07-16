import tkinter as tk
import faker
import pyperclip


class DataGeneratorApp:
    def __init__(self, root):
        self.region_var = None
        self.update_button = None
        self.data = None
        self.labels = None
        self.data_types = None
        self.fake_cn = faker.Faker('zh_CN')
        self.fake_en = faker.Faker('en_US')
        self.root = root
        self.root.title("数据生成器")
        self.create_widgets()
        self.update_data()

    def create_widgets(self):
        self.labels = {}
        self.data_types = [
            "姓名", "手机号", "性别", "银行卡号",
            "IP", "UUID", "邮箱", "地址"
        ]

        self.region_var = tk.StringVar(value="China")
        tk.Radiobutton(self.root, text="中国", variable=self.region_var, value="China").grid(row=0, column=0, sticky="w")
        tk.Radiobutton(self.root, text="海外", variable=self.region_var, value="Overseas").grid(row=0, column=1, sticky="w")

        for idx, data_type in enumerate(self.data_types, start=1):
            label = tk.Label(self.root, text=data_type)
            label.grid(row=idx, column=0, padx=10, pady=5)
            value_label = tk.Label(self.root, text="", relief="sunken")
            value_label.grid(row=idx, column=1, padx=10, pady=5, sticky="w")
            value_label.bind("<Button-1>", self.on_data_click)
            self.labels[data_type] = value_label

        self.update_button = tk.Button(self.root, text="更新所有数据", command=self.update_data)
        self.update_button.grid(row=len(self.data_types) + 1, column=0, columnspan=2, pady=10)

    def update_data(self):
        self.data = self.generate_data()

        for data_type, value in self.data.items():
            self.labels[data_type].config(text=value)

    def on_data_click(self, event):
        clicked_label = event.widget
        for data_type, label in self.labels.items():
            if label == clicked_label:
                new_value = self.generate_new_data(data_type)
                self.labels[data_type].config(text=new_value)
                pyperclip.copy(new_value)

    def generate_data(self):
        region = self.region_var.get()
        fake = self.fake_cn if region == "China" else self.fake_en

        return {
            "姓名": fake.name(),
            "手机号": fake.phone_number(),
            "性别": fake.random_element(elements=("男", "女")),
            "银行卡号": fake.credit_card_number(),
            "IP": fake.ipv4(),
            "UUID": fake.uuid4(),
            "邮箱": fake.email(),
            "地址": fake.address()
        }

    def generate_new_data(self, data_type):
        data = self.generate_data()
        return data[data_type]


if __name__ == "__main__":
    root = tk.Tk()
    app = DataGeneratorApp(root)
    root.mainloop()



