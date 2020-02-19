import os



def main():

    print("%03d" % 1)

    download_dir = "三年级语文下册"

    print(sorted(os.listdir(download_dir)))


if __name__ == '__main__':

    main()