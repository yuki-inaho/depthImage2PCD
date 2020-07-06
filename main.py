import cv2
import click
import toml
import open3d as o3d
from pathlib import Path
import pdb

SCRIPT_PATH = Path(__file__).resolve().parent
DEFAULT_DEPTH_IMG_PATH = str(Path(SCRIPT_PATH, "depth", "depth.png"))
DEFAULT_CONFIG_PATH = str(Path(SCRIPT_PATH, "cfg", "camera_parameter.toml"))
DEFAULT_PCD_OUTPUT_PATH = str(Path(SCRIPT_PATH, "pcd", "output.pcd"))

@click.command()
@click.option("--depth-image-path", "-d", default="{}".format(DEFAULT_DEPTH_IMG_PATH))
@click.option("--toml-path", "-t", default="{}".format(DEFAULT_CONFIG_PATH))
@click.option("--pcd-output-path", "-p", default="{}".format(DEFAULT_PCD_OUTPUT_PATH))
def main(depth_image_path, toml_path, pcd_output_path):
    depth_image = cv2.imread(depth_image_path, cv2.IMREAD_ANYDEPTH)
    depth_image[depth_image==65535] = 0
    depth_image_o3d = o3d.geometry.Image(depth_image)

    dict_toml = toml.load(open(toml_path))
    fx, fy, cx, cy = [
        dict_toml["Camera0_Factory"][elem] for elem in ["fx", "fy", "cx", "cy"]
    ]
    width, height = [
        dict_toml["Camera0"][elem] for elem in ["width", "height"]
    ]
    pinhole_camera_intrinsic = o3d.camera.PinholeCameraIntrinsic(
        width, height, fx, fy, cx, cy
    )
    pcd = o3d.geometry.PointCloud().create_from_depth_image(
        depth_image_o3d, pinhole_camera_intrinsic, depth_scale=1000.0
    )
    o3d.io.write_point_cloud(pcd_output_path, pcd)

if __name__ == "__main__":
    main()