from torchvision.datasets import MNIST
from torch.utils.data import Subset
import tqdm
import torch.utils
from hdc import *
import itertools
import PIL

MAX = 26


class MNISTClassifier:

    def __init__(self):
        self.classifier = HDItemMem()
        self.codebook = HDCodebook()

    def encode_coord(self, i, j):
        if not self.codebook.has(i):
            self.codebook.add(i)
        
        if not self.codebook.has(j):
            self.codebook.add(j)

        i_hv = self.codebook.get(i)
        j_hv = self.codebook.get(j)

        return HDC.bind(i_hv, HDC.permute(j_hv, 1))

    def encode_pixel(self, i, j, v):
        if not self.codebook.has(v):
            self.codebook.add(v)

        coord_hv = self.encode_coord(i, j)
        v_hv = self.codebook.get(v)

        return HDC.bind(coord_hv, HDC.permute(v_hv, 2))

    def encode_image(self, image):
        pixel_hvs = []

        for i, j in itertools.product(range(MAX), range(MAX)):
            v = image.getpixel((i, j))
            pixel_hv = HDC.permute(self.encode_pixel(i, j, v), i*MAX+j)
            pixel_hvs.append(pixel_hv)

        return HDC.bundle(pixel_hvs)

    def decode_pixel(self, image_hypervec, i, j):
        pixel_hv = HDC.permute(image_hypervec, -(i*MAX+j))
        coord_hv = self.encode_coord(i, j)

        value_hv = HDC.bind(pixel_hv, coord_hv)
        
        return self.codebook.wta(HDC.permute(value_hv, -2))

    def decode_image(self, image_hypervec):
        im = PIL.Image.new(mode="1", size=(MAX, MAX))
        for i, j in list(itertools.product(range(MAX), range(MAX))):
            v = self.decode_pixel(image_hypervec, i, j)
            im.putpixel((i, j), v)
        return im

    def train(self, train_data):
        for image, label in tqdm.tqdm(list(train_data)):
            raise Exception("do something with the image, label pair from the dataset")

    def classify(self, image):
        raise Exception("classify an image using your classifier and return the label and distance")
        return label, dist

    def build_gen_model(self, train_data):
        self.gen_model = {}
        for image, label in tqdm.tqdm(list(train_data)):
            raise Exception("build generative model")

    def generate(self, cat, trials=10):
        gen_hv = self.gen_model[cat]
        raise Exception("generate random image with label <cat> using generative model. Average over <trials> trials.")


def initialize(N=1000):
    alldata = MNIST(root='data', train=True, download=True)
    dataset = list(map(lambda datum: (datum[0].convert("1"), datum[1]),  \
                Subset(alldata, range(N))))

    train_data, test_data = torch.utils.data.random_split(dataset, [0.6, 0.4])
    HDC.SIZE = 10000
    classifier = MNISTClassifier()
    return train_data, test_data, classifier


def test_encoding():
    train_data, test_data, classifier = initialize()
    image0, _ = train_data[0]
    hv_image0 = classifier.encode_image(image0)
    result = classifier.decode_image(hv_image0)
    image0.save("sample0.png")
    result.save("sample0_rec.png")


def test_classifier():
    train_data, test_data, classifier = initialize(2000)

    print("======= training classifier =====")
    classifier.train(train_data)

    print("======= testing classifier =====")
    correct, count = 0, 0
    for image, category in (pbar := tqdm.tqdm(test_data)):
        cat, dist = classifier.classify(image)
        if cat == category:
            correct += 1
        count += 1

        pbar.set_description("accuracy=%f" % (float(correct)/count))

    print("ACCURACY: %f" % (float(correct)/count))

def test_generative_model():
    train_data, test_data, classifier = initialize(1000)
    print("======= building generative model =====")
    classifier.build_gen_model(train_data)

    print("======= generate images =====")
    while True:
        cat = random.randint(0, 9)
        img = classifier.generate(cat)
        print("generated image for class %d" % cat)
        img.save("generated.png")
        input("press any key to generate new image..")


if __name__ == '__main__':
    test_encoding()
    # test_classifier()
    # test_generative_model()
