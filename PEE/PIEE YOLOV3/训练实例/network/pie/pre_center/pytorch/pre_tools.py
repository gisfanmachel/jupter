import torch


def estimate_img(model,images,images2,cuda):
    with torch.no_grad():
        images = torch.from_numpy(images)
        if cuda:
            images = images.cuda()

        if images2 is not None:
            images2 = torch.from_numpy(images2)
            if cuda:
                images2 = images2.cuda()
            outputs = model(images,images2)
        else:
            outputs = model(images)

    return outputs