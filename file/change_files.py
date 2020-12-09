import argparse
import os
import shutil


def change_files(src_dir, src_exts, dst_prefix, dst_init_postfix, include_ext):
    if include_ext:
        for file in os.listdir(src_dir):
            ext = os.path.splitext(file)[1].replace('.', '')
            if ext in src_exts:
                change_file(os.path.join(src_dir, file),
                            os.path.join(src_dir, dst_prefix + '_' + str(dst_init_postfix) + '.' + ext))
                dst_init_postfix = dst_init_postfix + 1
    else:
        name_dict = {}
        for file in os.listdir(src_dir):
            split = os.path.splitext(file)
            ext = split[-1].replace('.', '')
            if ext in src_exts:
                if not split[0] in name_dict.keys():
                    name_dict[split[0]] = []
                name_dict[split[0]].append(file)

        os.mkdir(os.path.join(src_dir, 'tmp'))
        for file_list in name_dict.values():
            for file in file_list:
                shutil.copyfile(os.path.join(src_dir, file),
                                os.path.join(os.path.join(src_dir, 'tmp'),
                                             dst_prefix + '_' + str(dst_init_postfix) + os.path.splitext(file)[-1]))
                os.remove(os.path.join(src_dir, file))
            dst_init_postfix = dst_init_postfix + 1

        for file in os.listdir(os.path.join(src_dir, 'tmp')):
            shutil.move(os.path.join(os.path.join(src_dir, 'tmp'), file), src_dir)
        os.rmdir(os.path.join(src_dir, 'tmp'))


def change_file(src, dst):
    os.rename(src, dst)


# TODO: 바뀔 이름의 PREFIX, POSTFIX를 정하지 않고 고유 값 자체를 랜덤으로 생성해서 변환하는 기능 추가
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Change File Utility')

    parser.add_argument('--src_dir', type=str)  # 원본 디렉토리 위치
    parser.add_argument('--src_exts', type=str)  # 파일 이름을 바꿀 확장자들
    parser.add_argument('--dst_prefix', type=str)  # 바뀐 파일 이름의 프리픽스
    parser.add_argument('--dst_init_postfix', type=int)  # 바뀐 파일 이름의 포스트픽스 초기 값, 양의 정수

    def str2bool(value):
        if isinstance(value, bool):
            return value
        if value.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif value.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')

    parser.add_argument('--include_ext', type=str2bool)  # 이름 판단에 확장자 포함 여부

    args = parser.parse_args()

    print("Change file utility start. Source dir is %s" % args.src_dir)

    change_files(src_dir=args.src_dir, src_exts=[str(item) for item in args.src_exts.split(',')],
                 dst_prefix=args.dst_prefix, dst_init_postfix=args.dst_init_postfix,
                 include_ext=str2bool(args.include_ext))
