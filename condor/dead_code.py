import feature_flag
import settings


def hello_world():
    print('live')

    if feature_flag.is_active(settings.FEATURE_1):
        print('live')
        if feature_flag.is_active(settings.FEATURE_2):
            print('live')
            if feature_flag.is_active(settings.FEATURE_1):
                print('live')
            else:
                print('dead')
        else:
            print('dead')
        print('live')
        print('live')
        print('live')
        print('live')
    else:
        print('dead')


if __name__ == "__main__":
    hello_world()
