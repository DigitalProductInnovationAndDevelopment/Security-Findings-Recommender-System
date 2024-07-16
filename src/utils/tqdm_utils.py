from tqdm import tqdm


def conditional_tqdm(iterable, condition=True, **kwargs):
    if condition:
        return tqdm(iterable, **kwargs)
    return iterable
