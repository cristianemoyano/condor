import feature_flag
import settings


def hello_world():
    print('live')

    if feature_flag.is_active(settings.FEATURE_1) and 'other' == 'other':

        print('live partially')

        if feature_flag.is_active(settings.FEATURE_2):

            print('live')

            if feature_flag.is_active(settings.FEATURE_1) and 'other' == 'other':

                print('live')

            else:

                print('live partially')
        else:
            print('dead')

        if feature_flag.is_active(settings.FEATURE_1):

            print('live')

        else:

            print('dead')

        if 'other' == 'other' or feature_flag.is_active(settings.FEATURE_1):

            print('live')

        else:

            print('live partially')

        print('live')
        print('live')
        print('live')
        print('live')
    else:
        print('live partially')


if __name__ == "__main__":
    hello_world()
