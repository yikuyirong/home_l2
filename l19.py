import os
import re
from PIL import Image
import PyPDF2


def main():
    try:

        dir = input("输入文档所在的目录:")

        docs = input("输入需要组合的文档名称:")

        result = input("输入组合后的文件名:")

        if not os.path.isdir(dir):
            raise Exception(f"目录{dir}不存在")

        if docs == "":
            docs = os.listdir(dir)
        else:
            docs = re.split(r"\s+", docs)

        pdfs = []

        for doc in docs:

            doc_name = os.path.join(dir, doc)

            with Image.open(doc_name) as image:

                if image.mode != "RGB":
                    image = image.convert("RGB")

                pdf = f"{doc_name}.pdf"

                image.save(pdf, "PDF")

                pdfs.append(pdf)

        if len(pdfs):

            out_stream = PyPDF2.PdfFileWriter()

            for pdf in pdfs:
                reader = PyPDF2.PdfFileReader(pdf)
                out_stream.addPage(reader.getPage(0))

                # os.remove(pdf)

            out_stream.write(open(os.path.join(dir, result), "wb"))
            print("处理成功")

    except Exception as e:
        print("处理失败", str(e))

if __name__ == '__main__':
    main()
