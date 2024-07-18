import json
import random
import re
import time
import uuid

from src.arkose.session import FunCaptchaOptions
from src.utils.hash import x64hash128
from src.config import enforcement_hash

random.seed(int(time.time()))


def fake_user_agent_brands(ua):
    if "Edg" in ua:
        brand = "Chromium,Not(A:Brand,Microsoft Edge"
    elif "Chrome" in ua:
        brand = "Chromium,Not(A:Brand,Google Chrome"
    elif "Firefox" in ua:
        brand = None
    else:
        brand = "Not A(Brand,Chromium"
    return brand


def fake_network_info():
    speeds = [0.5, 1.35, 2.5, 5, 10]
    rtt_values = [50, 100, 150, 200, 300]
    return random.choice(speeds), random.choice(rtt_values)


def fake_battery_charging():
    return random.choice([True, False])


def fake_webgl_renderer():
    webgl_renders = ['Intel(R) HD Graphics', 'Adreno (TM) 540',
                     'ANGLE (NULL, Generic Renderer Direct3D11 vs_5_0 ps_5_0)', 'Generic Renderer',
                     'ANGLE (AMD, Radeon R9 200 Series Direct3D11 vs_5_0 ps_5_0)',
                     'ANGLE (AMD, Radeon HD 3200 Graphics Direct3D11 vs_5_0 ps_5_0)', 'Apple M1',
                     'ANGLE (Intel, Intel(R) HD Graphics 400 Direct3D11 vs_5_0 ps_5_0)', 'WebKit WebGL', 'llvmpipe',
                     'ANGLE (Intel, Intel(R) HD Graphics Direct3D11 vs_5_0 ps_5_0)', 'Adreno (TM) 650',
                     'ANGLE (NVIDIA, NVIDIA GeForce GTX 980 Direct3D11 vs_5_0 ps_5_0)', 'Radeon HD 3200 Graphics',
                     'Mali-G51', 'Mali-T628', 'Intel(R) HD Graphics 400']
    return random.choice(webgl_renders)


def fake_webgl_vendor():
    webgl_vendors = ['WebKit', 'Mozilla']
    return random.choice(webgl_vendors)


def fake_webgl_shading_language_version():
    webgl_shading_language_versions = ['WebGL GLSL ES 1.0 (1.20)', 'WebGL GLSL ES 1.0',
                                       'WebGL GLSL ES 1.0 (OpenGL ES GLSL ES 1.0 Chromium)', 'WebGL GLSL ES 1.0 (1.0)']
    return random.choice(webgl_shading_language_versions)


def fake_webgl_aliased_line_width_range():
    webgl_aliased_line_width_ranges = ['[1, 10]', '[1, 8]', '[1, 16]', '[1, 7.9921875]', '[1, 8191]', '[1, 31]',
                                       '[1, 2048]', '[1, 7.375]', '[1, 64]', '[1, 1]', '[1, 8192]', '[1, 255]',
                                       '[1, 100]', '[1, 4095.9375]', '[1, 7]']
    return random.choice(webgl_aliased_line_width_ranges)


def fake_webgl_aliased_point_size_range():
    webgl_aliased_point_size_ranges = ['[1, 511]', '[1, 256]', '[1, 64]', '[0.125, 8192]', '[1, 255.875]',
                                       '[1, 2047.9375]', '[1, 1023]', '[1, 8192]', '[1, 8191]', '[0.125, 2048]',
                                       '[1, 1024]', '[1, 2048]', '[1, 255]', '[1, 2047]', '[1, 100]']
    return random.choice(webgl_aliased_point_size_ranges)


def fake_webgl_antialiasing():
    webgl_antialiasings = ['no', 'yes']
    return random.choice(webgl_antialiasings)


def fake_webgl_max_params():
    webgl_max_params = ['16,48,4096,256,16384,16,4096,31,16,16,256', '16,48,4096,1024,16383,16,4096,31,16,16,1024',
                        '167,20,8192,220,8192,16,8192,9,16,4,253', '16,96,4096,256,16384,16,4096,31,16,16,256',
                        ',48,4096,1024,8192,16,4096,15,16,16,1024', '16,32,8192,1024,8192,16,8192,14,16,16,4095',
                        '16,20,8192,221,8192,16,8192,9,16,4,253', '16,20,16384,221,16384,16,16384,9,16,4,253',
                        '16,48,4096,1024,32768,16,4096,31,16,16,1024', ',96,4096,1024,4096,16,4096,15,16,16,1024',
                        '16,96,16384,256,16384,16,16384,32,32,16,256', '16,96,16384,256,16384,16,4096,31,32,16,256',
                        '16,32,16384,1024,8192,16,16384,31,16,16,1024', ',96,4096,4096,8192,16,4096,31,16,16,4096',
                        '16,32,16384,1024,16384,16,16384,15,16,16,1024', '16,64,16384,4096,8192,32,8192,31,16,32,4096',
                        '16,64,16384,4096,8192,16,8192,31,16,16,4096', '16,64,32768,1024,32768,32,32768,31,16,32,1024',
                        '16,32,8192,1024,8192,16,8192,15,16,16,1024', '16,255,16383,4096,16383,64,16383,31,32,64,4096',
                        '16,96,4096,4096,16383,16,4096,31,16,16,4096', '16,20,16384,220,16384,16,16384,9,16,4,253',
                        ',48,4096,1024,4096,16,4096,15,16,16,1024', '16,32,16384,1024,16384,16,16384,30,16,16,4095',
                        ',96,4096,1024,8192,16,4096,15,16,16,1024', '16,96,4096,256,16384,16,4096,31,32,16,256',
                        '16,384,8192,4096,16383,64,8192,31,32,64,4096', '16,192,8192,4096,8192,32,8192,32,16,32,4096',
                        '16,32,16384,1024,16384,16,16384,30,16,16,4096',
                        '16,32,16384,1024,16384,16,16384,32,16,16,1024', ',192,16384,4096,16384,32,16384,32,16,32,4096',
                        '16,384,4096,4096,16383,64,4096,31,32,64,4096', '16,32,16384,224,16384,16,16384,15,16,16,512',
                        '16,32,16384,1024,8192,16,16384,15,16,16,1024',
                        '16,768,4096,4096,16383,128,4096,31,32,128,4096', '16,64,4096,1024,16383,32,4096,31,16,32,1024',
                        '2,96,4096,256,4096,16,4096,15,16,16,256', '16,96,4096,4096,8192,16,4096,31,16,16,4096',
                        '16,80,8192,1024,8192,16,8192,32,16,16,1024', '16,192,16384,4096,16384,32,16384,32,16,32,4096',
                        '16,64,16384,4096,16384,32,16384,27,16,32,4096',
                        '16,64,16384,1024,16384,32,16384,32,16,32,1024', '16,16,16384,1024,8192,16,16384,32,16,16,1024',
                        '16,384,4096,4096,65536,64,4096,31,32,64,4096', ',128,8192,4096,8192,32,8192,32,16,32,4096',
                        '16,96,4096,1024,8192,16,4096,15,16,16,1024', '16,32,8192,1024,8192,16,8192,30,16,16,4095',
                        '16,96,4096,4096,32768,16,4096,31,32,16,4096', '16,32,16384,1024,16384,16,16384,30,16,16,1024',
                        ',96,4096,1024,8192,16,8192,15,16,16,1024', '16,64,16384,1024,16384,32,16384,31,16,32,1024',
                        '16,8,4096,64,4096,8,4096,8,16,8,128', ',96,4096,4096,16383,16,4096,31,32,16,4096',
                        '16,48,4096,1024,8192,16,4096,31,16,16,1024', '16,96,8192,4096,16383,16,8192,31,32,16,4096',
                        '16,96,8192,256,16384,16,8192,31,32,16,256', '16,96,16384,256,16384,16,16384,32,16,16,256',
                        '16,20,8192,220,8192,16,8192,9,16,4,253', '16,96,8192,256,8192,16,8192,17,16,16,256',
                        '16,96,4096,4096,32768,32,4096,31,16,32,4096', '16,384,4096,4096,32768,64,4096,31,32,64,4096',
                        '16,96,4096,4096,8192,16,8192,31,16,16,4096', '16,96,4096,4096,16383,16,4096,31,32,16,4096',
                        '16,192,32768,1024,32768,32,32768,32,16,32,1024', '16,32,16384,256,16384,16,16384,31,16,16,256',
                        '16,32,16384,1024,16384,16,16384,31,16,16,1024', '16,32,8192,261,8192,16,8192,32,32,16,256']
    return random.choice(webgl_max_params)


def fake_webgl_max_viewport_dims():
    webgl_max_viewport_dims = ['[8192, 8192]', '[16383, 16383]', '[4096, 4096]', '[32768, 32768]', '[16384, 16384]',
                               '[32767, 32767]']
    return random.choice(webgl_max_viewport_dims)


def fake_webgl_unmasked_vendor():
    webgl_unmasked_vendors = ['Google Inc. (NVIDIA)', 'ARM', 'Google Inc. (VMware)', 'Google Inc. (0x00001D17)',
                              'Google Inc. (AMD)', 'Google Inc. (Glenfly Tech Co. Ltd)',
                              'Google Inc. (AMD) #km6q0E5WHM', 'Google Inc. (0x344C5250)', 'Apple Inc.',
                              'Google Inc. (AMD) #6cI1zDD8Cn', 'Google Inc. (Intel)', 'Google Inc. (ARM)',
                              'Google Inc. (Apple)', 'Google Inc. (ATI Technologies Inc.)', 'Imagination Technologies',
                              'Intel', 'ATI Technologies Inc.', 'Google Inc. (Unknown)', 'Google Inc. (Intel Inc.)',
                              'Google Inc.', 'Google Inc. (AMD) #dekOCoaXGp', 'Mesa/X.org', 'Mesa',
                              'Google Inc. (Imagination Technologies)', 'Qualcomm', 'NVIDIA Corporation', 'Intel Inc.',
                              'Google Inc. (NVIDIA Corporation)', 'Google Inc. (Google)', 'Apple',
                              'Intel Open Source Technology Center', 'Google Inc. (Microsoft)',
                              'Google Inc. (Qualcomm)']
    return random.choice(webgl_unmasked_vendors)


def fake_webgl_unmasked_renderer():
    webgl_unmasked_renderers = ['ANGLE (NVIDIA, NVIDIA GeForce GT 720 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3090 Ti (0x00002203) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 (0x00001F0A) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'Mali-G57 MC2',
                                'ANGLE (Intel, Intel(R) UHD Graphics 750 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3050 Laptop GPU (0x000025A2) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 620 (0x00005917) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) HD Graphics 4400 Direct3D11 vs_5_0 ps_5_0, D3D11-20.19.15.5171)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 650 (0x00000FC6) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Ti Direct3D11 vs_5_0 ps_5_0, D3D11-31.0.15.3742)',
                                'ANGLE (Intel, Intel(R) HD Graphics (0x00000402) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NULL, Generic Renderer Direct3D11 vs_5_0 ps_5_0)',
                                'ANGLE (AMD, AMD Radeon(TM) Graphics Direct3D9Ex vs_3_0 ps_3_0, aticfx32.dll-31.0.14001.33004)',
                                'ANGLE (AMD, AMD Radeon 780M Graphics (0x000015BF) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Apple, Apple M2, OpenGL 4.1)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 (0x00002503) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel Inc., Intel(R) Iris(TM) Plus Graphics 640, OpenGL 4.1)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 670 Direct3D9Ex vs_3_0 ps_3_0, nvldumdx.dll)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GT 740 (0x00000FC8) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (AMD, AMD Radeon(TM) Vega 8 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA Corporation, NVIDIA GeForce RTX 3060/PCIe/SSE2, OpenGL 4.5.0)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GT 730 (0x00000F02) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'Apple M1',
                                'ANGLE (NVIDIA, NVIDIA Quadro P5000 (0x00001BB0) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Laptop GPU Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (AMD, AMD Radeon R7 200 Series (0x00006611) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce MX330 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 2080 (0x00001E87) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D9Ex vs_3_0 ps_3_0, igdumdim32.dll-27.20.100.9466)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 950 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'Mali-G720-Immortalis MC12',
                                'ANGLE (Intel, Intel(R) UHD Graphics 730 (0x00004C8B) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) HD Graphics 615 (0x0000591E) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (VMware, VMware SVGA 3D (0x00000405) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.101.1340)',
                                'ANGLE (AMD, AMD Radeon(TM) Graphics (0x00001638) Direct3D11 vs_5_0 ps_5_0, D3D11) #Y0yJGzXUlN',
                                'Google SwiftShader',
                                'ANGLE (Intel, Intel(R) UHD Graphics 730 (0x00004692) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3070 Laptop GPU (0x000024DD) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'Mali-G78', 'Adreno (TM) 640',
                                'ANGLE (Intel(R) UHD Graphics 600 Direct3D11 vs_5_0 ps_5_0)', 'Mali-G72',
                                'Adreno (TM) 660', 'ANGLE (NVIDIA, NVIDIA Quadro P400 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel(R) HD Graphics 400 Direct3D11 vs_5_0 ps_5_0)',
                                'ANGLE (AMD, AMD Radeon RX 640 (0x00006987) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 2060 (0x00001F15) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Laptop GPU (0x00002560) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3050 Laptop GPU (0x000025E2) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'Intel Iris OpenGL Engine',
                                'ANGLE (Intel, Intel(R) HD Graphics 4400 (0x0000041E) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Laptop GPU (0x00002520) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'Apple GPU',
                                'ANGLE (ATI Technologies Inc., AMD Radeon Pro 560X OpenGL Engine, OpenGL 4.1)',
                                'ANGLE (Google, Vulkan 1.2.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver-5.0.0)',
                                'ANGLE (Intel Inc., Intel(R) UHD Graphics 617, OpenGL 4.1)',
                                'ANGLE (NVIDIA GeForce GTX 1060 Direct3D11 vs_5_0 ps_5_0)',
                                'ANGLE (Apple, ANGLE Metal Renderer: Apple M2 Max, Unspecified Version)',
                                'ANGLE (NVIDIA GeForce RTX 2060 Direct3D11 vs_5_0 ps_5_0)',
                                'ANGLE (Intel, Intel(R) HD Graphics 4000 (0x00000166) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Qualcomm, Adreno (TM) 619, OpenGL ES 3.2)',
                                'ANGLE (Intel, Intel(R) HD Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) Iris(R) Xe Graphics (0x00009A49) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 2060 SUPER (0x00001F06) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 4060 Laptop GPU (0x000028E0) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) HD Graphics 4000 Direct3D9Ex vs_3_0 ps_3_0, igdumd64.dll)',
                                'ANGLE (NVIDIA, NVIDIA GeForce MX550 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) HD Graphics Direct3D9Ex vs_3_0 ps_3_0, igdumdim64.dll)',
                                'ANGLE (Intel, Intel(R) UHD Graphics (0x00009BC4) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel Inc., Intel(R) Iris(TM) Plus Graphics OpenGL Engine, OpenGL 4.1)',
                                'ANGLE (AMD, AMD Radeon(TM) Graphics Direct3D9Ex vs_3_0 ps_3_0, aticfx64.dll)',
                                'ANGLE (AMD, Radeon RX550/550 Series Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA Quadro P400 (0x00001CB3) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics (0x00009BCA) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) HD Graphics 510 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 750 Ti (0x00001380) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 630 (0x00003E98) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1050 Ti Direct3D9Ex vs_3_0 ps_3_0, nvd3dumx.dll)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3070 (0x00002488) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (AMD, AMD Radeon 780M Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (AMD, AMD Radeon(TM) Vega 8 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11-26.20.12020.3002)',
                                'ANGLE (Intel, Mesa Intel(R) Graphics (ADL GT2), OpenGL 4.6)',
                                'ANGLE (AMD, AMD Radeon(TM) RX Vega 10 Graphics (0x000015D8) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Qualcomm, Adreno (TM) 620, OpenGL ES 3.2)',
                                'ANGLE (AMD, Radeon RX 570 Series Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.15002.1004)',
                                'ANGLE (AMD, AMD Radeon(TM) Vega 8 Graphics (0x000015DD) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) Q45/Q43 Express Chipset (Microsoft Corporation - WDDM 1.1) Direct3D9Ex vs_3_0 ps_3_0, igdumd64.dll)',
                                'ANGLE (Google, Vulkan 1.2.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.100.9316)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 770 (0x00004690) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics (0x00004628) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1050 Ti Direct3D11 vs_5_0 ps_5_0, D3D11-27.21.14.5709)',
                                'Mali-G57', 'Adreno (TM) 620',
                                'ANGLE (Intel, Intel(R) Iris(R) Xe Graphics Direct3D11 vs_5_0 ps_5_0, D3D11-31.0.101.3251)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 (0x00002504) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) HD Graphics Direct3D11 vs_5_0 ps_5_0)', 'Adreno (TM) 619',
                                'ANGLE (Intel, Intel(R) HD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 610 (0x00003E90) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Glenfly Tech Co. Ltd, Glenfly Arise1020, OpenGL 4.5)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1080 Direct3D11 vs_5_0 ps_5_0, D3D11)', 'Mali-G71',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 4060 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3050 Ti Laptop GPU Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics (0x0000A720) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'GeForce GTX 980/PCIe/SSE2',
                                'ANGLE (AMD, AMD Radeon RX 6750 GRE 12GB (0x000073DF) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11-31.0.101.2111)',
                                'ANGLE (NVIDIA GeForce GTX 1050 Direct3D11 vs_5_0 ps_5_0)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 950M Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 770 (0x00004680) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'llvmpipe',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 2070 with Max-Q Design (0x00001F14) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 730 (0x00004682) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel(R) HD Graphics 4000 Direct3D9Ex vs_3_0 ps_3_0)',
                                'Intel HD Graphics 5000 OpenGL Engine', 'Mali-G710 MC10',
                                'ANGLE (ARM, Mali-G57 MC2, OpenGL ES 3.2)',
                                'ANGLE (Qualcomm, Adreno (TM) 640, OpenGL ES 3.2)',
                                'ANGLE (Intel, Intel(R) HD Graphics 4400 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Apple, ANGLE Metal Renderer: Apple M2, Unspecified Version)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 960 (0x00001401) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GT 730 (0x00001287) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1050 with Max-Q Design Direct3D11 vs_5_0 ps_5_0, D3D11-31.0.15.4633)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'Intel(R) HD Graphics 400',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1070 (0x00001B81) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA Corporation, NVIDIA GeForce GT 750M OpenGL Engine, OpenGL 4.1)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 4060 Ti (0x00002805) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1660 Ti (0x00002182) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics (0x00004E61) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) Iris(R) Plus Graphics Direct3D9Ex vs_3_0 ps_3_0, igdumdim32.dll-27.20.100.9621)',
                                'ANGLE (Intel, Intel(R) HD Graphics 630 (0x00005912) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) HD Graphics 615 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (AMD, AMD Radeon(TM) Vega 8 Graphics (0x000015D8) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA Quadro M5000 Direct3D11 vs_5_0 ps_5_0, D3D11-21.21.13.7651)',
                                'ANGLE (ARM, Mali-G720-Immortalis MC12, OpenGL ES 3.2)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 630 (0x00003E91) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'Adreno (TM) 509', 'PowerVR SGX Maca',
                                'ANGLE (Intel, Intel(R) HD Graphics 5500 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1060 Direct3D11 vs_5_0 ps_5_0, D3D11-27.21.14.5148)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3050 (0x00002582) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (AMD, AMD Radeon(TM) R7 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 730 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (AMD, AMD Radeon RX 580 2048SP (0x00006FDF) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (ARM, Mali-G710 MC10, OpenGL ES 3.2)',
                                'ANGLE (AMD, AMD Radeon RX 6600 Direct3D11 vs_5_0 ps_5_0, D3D11-31.0.22023.1014)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Ti (0x00002489) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Apple, ANGLE Metal Renderer: Apple M1 Pro, Unspecified Version)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 (0x00001F91) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'Adreno (TM) 642L',
                                'ANGLE (AMD, AMD Radeon(TM) Graphics (0x00001638) Direct3D11 vs_5_0 ps_5_0, D3D11) #O0LeLwhSct',
                                'Adreno (TM) 720', 'Mali-G715-Immortalis MC11',
                                'ANGLE (AMD, AMD Radeon HD 7700 Series (0x0000683F) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GT 730 Direct3D11 vs_5_0 ps_5_0, D3D11-27.21.14.5671)',
                                'Apple M2', 'ANGLE (ARM, Mali-G76, OpenGL ES 3.2)',
                                'ANGLE (ARM, Mali-G52 MC2, OpenGL ES 3.2)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 770 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'Adreno (TM) 644', 'ANGLE (NVIDIA GeForce GT 610  Direct3D11 vs_5_0 ps_5_0)',
                                'Adreno (TM) 725',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1660 Ti Direct3D11 vs_5_0 ps_5_0, D3D11-31.0.15.1700)',
                                'ANGLE (NVIDIA GeForce GT 240 Direct3D11 vs_4_1 ps_4_1)',
                                'ANGLE (Intel, Intel(R) HD Graphics Family (0x00000A16) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) HD Graphics 530 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1050 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'Adreno (TM) 650 d',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 (0x00001F99) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel Inc., Intel(R) UHD Graphics 630, OpenGL 4.1)',
                                'ANGLE (NVIDIA, NVIDIA Quadro RTX 4000 (0x00001EB1) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) HD Graphics 3000 Direct3D9Ex vs_3_0 ps_3_0, igdumd64.dll)',
                                'ANGLE (Intel, Mesa Intel(R) UHD Graphics 630 (CFL GT2), OpenGL 4.6)',
                                'ANGLE (Intel, Mesa Intel(R) Graphics (RPL-S), OpenGL 4.6)',
                                'ANGLE (Intel, Intel(R) HD Graphics Direct3D9Ex vs_3_0 ps_3_0, igdumd64.dll)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3050 Laptop GPU Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA GeForce RTX 4070 Laptop GPU Direct3D11 vs_5_0 ps_5_0)',
                                'ANGLE (AMD, AMD Radeon (TM) Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel(R) HD Graphics 4400 Direct3D11 vs_5_0 ps_5_0)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3050 Ti Laptop GPU (0x000025A0) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'PowerVR Rogue GE8320',
                                'ANGLE (AMD, AMD Radeon(TM) Graphics (0x00001638) Direct3D11 vs_5_0 ps_5_0, D3D11) #4I43ROvRJl',
                                'ANGLE (Intel, Intel(R) UHD Graphics 750 (0x00004C8A) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA Quadro P2000 (0x00001C30) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'AMD Radeon Pro 560X OpenGL Engine',
                                'ANGLE (Intel, Intel(R) HD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.100.8682)',
                                'ANGLE (ARM, Mali-G610 MC6, OpenGL ES 3.2)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 4060 Ti (0x00002803) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 Ti Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) HD Graphics 6000 (0x00001626) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Apple, Apple M1, OpenGL 4.1)',
                                'ANGLE (ATI Technologies Inc., AMD Radeon Pro 580X OpenGL Engine, OpenGL 4.1)',
                                'ANGLE (Intel, Intel(R) UHD Graphics (0x00009A78) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA Quadro P620 Direct3D9Ex vs_3_0 ps_3_0, nvd3dumx.dll)',
                                'ANGLE (AMD, AMD Radeon(TM) Graphics Direct3D11 vs_5_0 ps_5_0, D3D11-31.0.12044.3)',
                                'Mali-G76', 'Intel(R) HD Graphics',
                                'ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.100.9864)',
                                'ANGLE (ATI Technologies Inc., AMD Radeon Pro 450 OpenGL Engine, OpenGL 4.1)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D9Ex vs_3_0 ps_3_0, igdumdim32.dll-27.20.100.8681)',
                                'Adreno (TM) 630',
                                'ANGLE (NVIDIA, NVIDIA GeForce GT 730 Direct3D11 vs_5_0 ps_5_0, D3D11-26.21.14.3650)',
                                'ANGLE (AMD Radeon(TM) Graphics Direct3D11 vs_5_0 ps_5_0)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GT 740 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 Direct3D9Ex vs_3_0 ps_3_0, nvldumd.dll-31.0.15.1700)',
                                'PowerVR SGX Auckland',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 2060 (0x00001F03) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1660 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (AMD, AMD Radeon(TM) Graphics (0x00001681) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics (0x0000468B) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) Iris(R) Plus Graphics (0x00008A52) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Qualcomm, Adreno (TM) 642L, OpenGL ES 3.2)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 (0x00002544) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA GeForce GT 710 Direct3D11 vs_5_0 ps_5_0)',
                                'ANGLE (AMD, AMD Radeon R7 200 Series Direct3D9Ex vs_3_0 ps_3_0, aticfx32.dll-23.20.15033.5003)',
                                'ANGLE (Intel, Intel(R) Iris(R) Plus Graphics Direct3D11 vs_5_0 ps_5_0, D3D11-26.20.100.7926)',
                                'ANGLE (NVIDIA, NVIDIA Quadro P620 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics (0x0000A721) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1050 Ti Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA Quadro M1200 (0x000013B6) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (AMD, Radeon RX 550X (0x0000699F) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3070 (0x00002484) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'Adreno (TM) 750', 'ANGLE (Intel, Mesa Intel(R) Graphics (ADL-S GT1), OpenGL 4.6)',
                                'ANGLE (Intel(R) UHD Graphics Direct3D11 vs_5_0 ps_5_0)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Ti Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3080 Laptop GPU (0x000024DC) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GT 730   Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Apple, Apple M2 Pro, OpenGL 4.1)',
                                'ANGLE (Intel, Intel(R) UHD Graphics Direct3D9Ex vs_3_0 ps_3_0, igd10iumd32.dll-31.0.101.4502)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 630 (0x00003E92) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce 210  (0x00000A65) Direct3D11 vs_4_1 ps_4_1, D3D11)',
                                'Radeon HD 3200 Graphics', 'PowerVR Rogue GE8300',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1050 with Max-Q Design Direct3D11 vs_5_0 ps_5_0, D3D11-26.21.14.4141)',
                                'ANGLE (Intel, Intel(R) HD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Qualcomm, Adreno (TM) 660, OpenGL ES 3.2)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 4060 Laptop GPU Direct3D11 vs_5_0 ps_5_0, D3D11-31.0.15.4584)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 750 Ti Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics (0x00004C8B) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'Adreno (TM) 616',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1060 3GB (0x00001C02) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1660 SUPER (0x000021C4) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) HD Graphics 4600 Direct3D9Ex vs_3_0 ps_3_0, igdumdim64.dll)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1070 (0x00001BE1) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (ATI Technologies Inc., AMD Radeon Pro 5300M OpenGL Engine, OpenGL 4.1)',
                                'ANGLE (Intel Inc., Intel(R) Iris(TM) Plus Graphics 655, OpenGL 4.1)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 2060 SUPER Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 2060 SUPER Direct3D9Ex vs_3_0 ps_3_0, nvldumd.dll-31.0.15.3713)',
                                'ANGLE (AMD, RENOIR (radeonsi renoir LLVM 15.0.7), OpenGL 4.6)',
                                'ANGLE (AMD, AMD Radeon RX 6650 XT (0x000073EF) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1060 (0x00001C20) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'Jingjia JM9230',
                                'ANGLE (Intel, Intel(R) HD Graphics 4600 (0x00000412) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.100.9664)',
                                'ANGLE (Intel, Intel(R) Iris(R) Xe Graphics (0x0000A7A0) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 2070 (0x00001F02) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D9Ex vs_3_0 ps_3_0, igdumdim32.dll-31.0.101.2111)',
                                'ANGLE (Intel, Intel(R) Iris(R) Xe Graphics (0x000046A8) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'Adreno (TM) 720 S', 'ANGLE (Intel(R) HD Graphics P630 Direct3D11 vs_5_0 ps_5_0)',
                                'ANGLE (Intel, Intel(R) HD Graphics 630 Direct3D9Ex vs_3_0 ps_3_0, igdumdim32.dll-31.0.101.2111)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1050 (0x00001C81) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics Direct3D11 vs_5_0 ps_5_0, D3D11-31.0.101.2125)',
                                'ANGLE (ATI Technologies Inc., AMD Radeon Pro 560 OpenGL Engine, OpenGL 4.1)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1070 Ti Direct3D11 vs_5_0 ps_5_0, D3D11-31.0.15.3667)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 730 (0x00004C8B) Direct3D11on12 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel(R) Iris(R) Plus Graphics 655 Direct3D11 vs_5_0 ps_5_0)',
                                'ANGLE (AMD, AMD Radeon RX 6700 XT (0x000073DF) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3080 Ti Laptop GPU (0x00002420) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) HD Graphics 630 (0x0000591B) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'Mali-G57 MC3', 'AMD Radeon Pro 5300M OpenGL Engine',
                                'ANGLE (NVIDIA, NVIDIA GeForce GT 710 (0x0000128B) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'Mali-G610 MC6',
                                'ANGLE (Intel, Intel(R) HD Graphics Family Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'NVIDIA GeForce GTX 980/PCIe/SSE2',
                                'ANGLE (AMD, AMD Radeon(TM) Graphics (0x00001638) Direct3D11 vs_5_0 ps_5_0, D3D11) #R4ugT6nbAB',
                                'ANGLE (NVIDIA, NVIDIA Quadro P1000 (0x00001CB1) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (AMD, AMD Radeon RX 6500 XT (0x0000743F) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics (0x00009BA4) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3050 Laptop GPU Direct3D11 vs_5_0 ps_5_0, D3D11-31.0.15.2892)',
                                'ANGLE (ARM, Mali-G715-Immortalis MC11, OpenGL ES 3.2)',
                                'ANGLE (Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0)',
                                'ANGLE (AMD, Radeon HD 3200 Graphics Direct3D11 vs_5_0 ps_5_0)',
                                'ANGLE (Intel(R) HD Graphics 5500 Direct3D11 vs_5_0 ps_5_0)', 'Mali-G52 MC2',
                                'ANGLE (Intel, Intel(R) UHD Graphics (0x00008A56) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (AMD, AMD Radeon HD 6700 Series (0x000068BA) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GT 1030 (0x00001D01) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (AMD, AMD Radeon R7 Graphics Direct3D9Ex vs_3_0 ps_3_0, aticfx64.dll)',
                                'ANGLE (Intel, Intel(R) Iris(R) Xe Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) Iris(R) Xe Graphics (0x000046A6) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (ATI Technologies Inc., AMD Radeon Pro 555X OpenGL Engine, OpenGL 4.1)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Laptop GPU Direct3D11 vs_5_0 ps_5_0, D3D11-31.0.15.3168)',
                                'Adreno (TM) 650',
                                'ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11-31.0.101.2111)',
                                'ANGLE (AMD, AMD Radeon R7 200 Series (0x00006613) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1080 Ti (0x00001B06) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 610 (0x00009BA8) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics (0x00004E55) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 630 (0x00009BC5) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 620 (0x00003EA0) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) Iris(R) Xe Graphics Direct3D9Ex vs_3_0 ps_3_0, igdumdim32.dll-31.0.101.4502)',
                                'ANGLE (Intel, Intel(R) HD Graphics 620 (0x00005916) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce MX450 (0x00001F97) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 610 Direct3D9Ex vs_3_0 ps_3_0, igdumdim32.dll-30.0.101.1994)',
                                'ANGLE (NVIDIA, NVIDIA Quadro P2000 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.101.1404)',
                                'ANGLE (ATI Technologies Inc., AMD Radeon RX 580 OpenGL Engine, OpenGL 4.1)',
                                'ANGLE (ATI Technologies Inc., AMD Radeon Pro 5500M OpenGL Engine, OpenGL 4.1)',
                                'ANGLE (AMD, AMD Radeon(TM) Graphics (0x0000164C) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 650 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics (0x00009A60) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (AMD, RENOIR (renoir LLVM 15.0.7), OpenGL 4.6)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3090 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'Mali-G57 MC5', 'ANGLE (Apple, ANGLE Metal Renderer: Apple M1, Unspecified Version)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3050 Ti Laptop GPU (0x000025E0) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (AMD, AMD Radeon(TM) Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (ARM, Mali-G77 MC9, OpenGL ES 3.2)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 710 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (AMD, AMD Radeon (TM) Graphics (0x000015E7) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (AMD, AMD Radeon(TM) Graphics (0x00001638) Direct3D11 vs_5_0 ps_5_0, D3D11) #9SdwNsmVJw',
                                'ANGLE (NVIDIA, NVIDIA T1000 (0x00001FB0) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1660 (0x00002184) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (AMD, AMD Radeon RX 580 2048SP Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'Adreno (TM) 740',
                                'ANGLE (Intel, Intel(R) HD Graphics 530 (0x00001912) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'Adreno (TM) 506', 'Mali-G72 MP3', 'Adreno (TM) 610',
                                'ANGLE (Qualcomm, Adreno (TM) 650, OpenGL ES 3.2)',
                                'ANGLE (Intel, Intel(R) HD Graphics 4600 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3080 Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.14.7212)',
                                'ANGLE (Intel, Intel(R) HD Graphics 4600 (0x00000416) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) HD Graphics 400 Direct3D11 vs_5_0 ps_5_0)',
                                'ANGLE (AMD, AMD Radeon(TM) Vega 10 Mobile Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (AMD, AMD Radeon(TM) Graphics (0x00001638) Direct3D11 vs_5_0 ps_5_0, D3D11) #A0O7mSskTc',
                                'ANGLE (Intel, Intel(R) HD Graphics 530 Direct3D9Ex vs_3_0 ps_3_0, igdumdim64.dll)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 2070 (0x00001F07) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) Iris(TM) Graphics 5100 Direct3D9Ex vs_3_0 ps_3_0, aticfx64.dll)',
                                'Maleoon 910',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 2060 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics (0x00004626) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GT 620 (0x00001049) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics (0x00009A68) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1050 (0x00001C8D) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 2060 (0x00001F11) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel(R) HD Graphics 610 Direct3D11 vs_5_0 ps_5_0)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 610 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) HD Graphics 520 (0x00001916) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Qualcomm, Adreno (TM) 730, OpenGL ES 3.2)',
                                'ANGLE (Intel, Intel(R) Iris(R) Plus Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 (0x00002188) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel Inc., Intel Iris Pro OpenGL Engine, OpenGL 4.1)',
                                'ANGLE (AMD, AMD Radeon(TM) Graphics (0x00001638) Direct3D11 vs_5_0 ps_5_0, D3D11) #g3ysWeSCbF',
                                'ANGLE (Apple, ANGLE Metal Renderer: Apple M3 Max, Unspecified Version)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.100.9805)',
                                'ANGLE (AMD, Radeon RX 350 Series (0x0000154C) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 630 (0x00003E9B) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 2080 Ti (0x00001E07) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA NVS 4200M    Direct3D9Ex vs_3_0 ps_3_0)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 4090 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 950 (0x00001402) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Apple, Apple M1 Pro, OpenGL 4.1)',
                                'ANGLE (Intel Inc., Intel(R) HD Graphics 630, OpenGL 4.1)',
                                'ANGLE (AMD, Radeon 520 (0x00006611) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA Quadro P620 (0x00001CB6) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (AMD, AMD Radeon RX590 GME (0x00006FDF) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (AMD, AMD Radeon(TM) Graphics (0x00001638) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GT 610 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics 630 (0x00009BC8) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) Iris(R) Plus Graphics (0x00008A51) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1660 Ti (0x00002191) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (AMD, AMD Radeon(TM) 780M Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) HD Graphics 610 (0x00005902) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 960 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics (0x0000A788) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (AMD, AMD Radeon RX 6600 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 4070 (0x00002786) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) HD Graphics 3000 Direct3D9Ex vs_3_0 ps_3_0, aticfx64.dll-8.17.10.1404)',
                                'ANGLE (NVIDIA GeForce GTX 1650 Direct3D11 vs_5_0 ps_5_0)',
                                'ANGLE (Intel, Intel(R) HD Graphics 4000 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Apple, ANGLE Metal Renderer: Apple M2 Pro, Unspecified Version)',
                                'ANGLE (ARM, Mali-G52, OpenGL ES 3.2)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1060 6GB (0x00001C03) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) HD Graphics 530 (0x0000191B) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 4050 Laptop GPU (0x000028E1) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'PowerVR SGX Doma',
                                'ANGLE (Intel, Intel(R) UHD Graphics (0x000046A3) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (AMD, Radeon R9 200 Series Direct3D11 vs_5_0 ps_5_0)', 'Mali-G52',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 4060 Laptop GPU (0x000028A0) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 4090 (0x00002684) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce 9500 GT (0x00000640) Direct3D11 vs_4_0 ps_4_0, D3D11)',
                                'ANGLE (Intel, Intel(R) HD Graphics 5500 (0x00001616) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'Adreno (TM) 618', 'ANGLE (Intel(R) Iris(R) Xe Graphics Direct3D11 vs_5_0 ps_5_0)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 (0x00002487) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (ARM, Mali-G715, OpenGL ES 3.2)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Laptop GPU Direct3D11 vs_5_0 ps_5_0, D3D11-31.0.15.4633)',
                                'Adreno (TM) 510', 'ANGLE (Qualcomm, Adreno (TM) 740, OpenGL ES 3.2)', 'Mali-G68 MC4',
                                'ANGLE (Intel, Intel(R) UHD Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1060 6GB Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Qualcomm, Adreno (TM) 750, OpenGL ES 3.2)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 2060 (0x00001F08) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, ANGLE Metal Renderer: Intel(R) UHD Graphics 630, Unspecified Version)',
                                'ANGLE (NVIDIA Quadro P620 Direct3D11 vs_5_0 ps_5_0)', 'Mali-G68',
                                'ANGLE (NVIDIA Corporation, NVIDIA GeForce RTX 2060/PCIe/SSE2, OpenGL 4.5.0)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1050 Ti (0x00001C82) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics Direct3D9Ex vs_3_0 ps_3_0, igdumdim32.dll-27.20.100.9365)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 760 (0x00001187) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 2070 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'Adreno (TM) 730',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1050 with Max-Q Design (0x00001C8D) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel Inc., Intel(R) Iris(TM) Graphics 6100, OpenGL 4.1)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 Ti (0x00001F95) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (ARM, Mali-G77, OpenGL ES 3.2)',
                                'ANGLE (AMD, AMD Radeon R9 255 (0x00006835) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 2070 SUPER (0x00001E84) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GT 730 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics (0x00009B41) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) UHD Graphics Direct3D9Ex vs_3_0 ps_3_0, igdumdim32.dll-27.20.100.8984)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 980 Direct3D11 vs_5_0 ps_5_0)', 'Adreno (TM) 710',
                                'ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver)',
                                'ANGLE (NVIDIA GeForce GT 730 Direct3D11 vs_5_0 ps_5_0)', 'Adreno (TM) 512',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3050 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (AMD, AMD Radeon(TM) Graphics (0x00001636) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel(R) HD Graphics 620 Direct3D11 vs_5_0 ps_5_0)',
                                'ANGLE (Intel, Intel(R) HD Graphics Direct3D11 vs_4_1 ps_4_1, D3D11)', 'Mali-G77 MC9',
                                'ANGLE (Apple, ANGLE Metal Renderer: Apple M3 Pro, Unspecified Version)',
                                'ANGLE (Intel, Intel(R) UHD Graphics (0x0000A7A8) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'Mali-G51', 'NVIDIA GeForce GT 730/PCIe/SSE2',
                                'ANGLE (Intel(R) UHD Graphics 750 Direct3D11 vs_5_0 ps_5_0)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 750 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA Quadro K2000  (0x00000FFE) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) HD Graphics 610 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GT 1030 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (AMD, AMD Radeon(TM) 610M Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3090 (0x00002204) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel, Intel(R) HD Graphics 520 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 (0x00001F82) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'Adreno (TM) 650 )', 'Mali-G77',
                                'ANGLE (Intel Inc., Intel(R) HD Graphics 6000, OpenGL 4.1)',
                                'ANGLE (NVIDIA GeForce RTX 4060 Direct3D11 vs_5_0 ps_5_0)',
                                'ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Ti (0x000024C9) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel Inc., Intel(R) Iris(TM) Plus Graphics 645, OpenGL 4.1)',
                                'ANGLE (Intel, Intel(R) UHD Graphics Direct3D11 vs_5_0 ps_5_0, D3D11-31.0.101.3616)',
                                'ANGLE (Apple, ANGLE Metal Renderer: Apple M1 Max, Unspecified Version)',
                                'ANGLE (NVIDIA, NVIDIA T400 4GB (0x00001FF2) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                                'ANGLE (Intel(R) HD Graphics 630 Direct3D11 vs_5_0 ps_5_0)',
                                'ANGLE (Intel Inc., Intel(R) Iris(TM) Plus Graphics OpenGL Engine (1x6x8 (fused) LP, OpenGL 4.1)']
    return random.choice(webgl_unmasked_renderers)


def fake_webgl_vsf_params():
    webgl_vsf_params = ['23,127,127,10,15,15,10,15,15', '23,127,127,10,14,14,8,1,1', '23,127,127,23,127,127,23,127,127']
    return random.choice(webgl_vsf_params)


def fake_webgl_vsi_params():
    webgl_vsi_params = ['0,24,24,0,24,24,0,24,24', '0,31,30,0,15,14,0,15,14', '0,31,31,0,15,15,0,15,15',
                        '0,31,31,0,31,31,0,31,31', '0,31,30,0,31,30,0,31,30']
    return random.choice(webgl_vsi_params)


def fake_webgl_fsf_params():
    webgl_fsf_params = ['23,127,127,10,15,15,10,15,15', '23,127,127,10,14,14,8,1,1', '0,0,0,10,15,15,10,15,15',
                        '23,127,127,23,127,127,23,127,127']
    return random.choice(webgl_fsf_params)


def fake_webgl_fsi_params():
    webgl_fsi_params = ['0,31,30,0,15,14,0,15,14', '0,24,24,0,24,24,0,24,24', '0,31,30,0,31,30,0,31,30',
                        '0,31,31,0,15,15,0,15,15']
    return random.choice(webgl_fsi_params)


navigator_connection_downlink_list = [0.7, 1.75, 2.3, 3.25, 1.3, 5.95, 6.75, 5.2, 8.45, 9.75, 10, 8.8, 5.6, 8.9, 9.6, 9,
                                      7.8, 9.35, 9.3, 2.75, 3.75,
                                      4, 4.25, 4.75, 4.5, 3.5, 5, 5.25, 5.5, 5.75, 1.5, 1.25, 6, 1, 0.25, 7.75, 7, 0.5,
                                      6.5, 6.25, 8.5, 8.75, 8, 7.5,
                                      8.25, 9.25, 9.5, 8.05, 2.5, 2, 2.25, 3, 1.4, 1.15, 1.9, 1.65, 2.65, 2.15, 2.9,
                                      2.4, 3.65, 3.9, 3.15, 3.4, 3.55,
                                      0.45, 4.3, 4.65, 4.9, 4.15, 4.4, 5.4, 5.15, 5.65, 0.75, 5.9, 6.15, 6.65, 6.9, 7.9,
                                      7.4, 7.65, 7.15, 8.15, 8.65,
                                      9.15, 9.4, 9.9, 9.65, 0.15, 2.8, 2.05, 2.55, 3.05, 0.8, 3.8, 3.3, 0.55, 4.8, 1.55,
                                      4.55, 1.8, 1.05, 5.55, 5.3,
                                      5.05, 5.8, 4.05, 6.3, 6.55, 6.05, 6.8, 7.3, 7.05, 7.55, 0.6, 0.4, 0.85, 0.65, 0.9,
                                      7.1, 0.35, 7.35, 1.85, 8.85,
                                      8.2, 8.7, 8.55, 8.3, 8.95, 9.7, 9.2, 9.8, 0.95, 9.95, 9.55, 9.05, 1.45, 1.2, 1.7,
                                      1.95, 2.7, 2.95, 2.45, 2.2,
                                      3.95, 3.7, 3.45, 3.2, 4.2, 4.7, 4.45, 4.95, 5.45, 5.7, 6.95, 6.7, 6.45, 6.2, 7.7,
                                      7.45, 7.2, 7.95, 0.3, 4.85,
                                      4.1, 4.6, 4.35, 5.1, 5.35, 5.85, 6.6, 6.1, 6.35, 6.85, 7.6, 7.85, 1.35, 1.6, 1.1,
                                      8.6, 8.35, 2.85, 2.1, 2.35,
                                      9.85, 9.1, 3.85, 3.6, 2.6, 3.35, 3.1]

network_info_rtt_list = [900, 650, 400, 1300, 150, 800, 550, 300, 50, 3000, 700, 450, 200, 850, 600, 350, 100, 1000,
                         750, 500, 250]


# 定义一个函数来模拟不同的音频编解码器支持
def fake_audio_codecs_support():
    codecs = {
        "ogg": random.choice(["probably", "maybe", ""]),
        "mp3": random.choice(["probably", "maybe", ""]),
        "wav": random.choice(["probably", "maybe", ""]),
        "m4a": random.choice(["probably", "maybe", ""]),
        "aac": random.choice(["probably", "maybe", ""])
    }
    return json.dumps(codecs)


# 定义一个函数来模拟不同的视频编解码器支持
def fake_video_codecs_support():
    codecs = {
        "ogg": random.choice(["probably", "maybe", ""]),
        "h264": random.choice(["probably", "maybe", ""]),
        "webm": random.choice(["probably", "maybe", ""]),
        "mpeg4v": random.choice(["probably", "maybe", ""]),
        "mpeg4a": random.choice(["probably", "maybe", ""]),
        "theora": random.choice(["probably", "maybe", ""])
    }
    return json.dumps(codecs)


def fake_video_codecs_extended():
    video_codecs_extendeds = [
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":true},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"maybe","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"maybe","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"maybe","mediaSource":false},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"maybe","mediaSource":false},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"maybe","mediaSource":false},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"maybe","mediaSource":false},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"maybe","mediaSource":false},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"maybe","mediaSource":false},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp8\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp9\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"","mediaSource":false},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"probably","mediaSource":true}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":null},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":null},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"probably","mediaSource":null},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"","mediaSource":null},"video/webm; codecs=\\"vp8\\"":{"canPlay":"","mediaSource":null},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"","mediaSource":null},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"","mediaSource":null},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"","mediaSource":null},"video/webm; codecs=\\"vp9\\"":{"canPlay":"","mediaSource":null},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"","mediaSource":null},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"","mediaSource":null},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":null},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":null},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":null},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":null},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":null},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":null},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":null},"video/ogg; codecs=\\"flac\\"":{"canPlay":"","mediaSource":null},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"probably","mediaSource":null}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":true},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"probably","mediaSource":true}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":true},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"probably","mediaSource":null},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":null},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":null},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":null},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":null},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":null},"video/webm; codecs=\\"vp9\\"":{"canPlay":"","mediaSource":null},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"","mediaSource":null},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"","mediaSource":null},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":null},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":null},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":null},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":null},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":null},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":null},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":null},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":null},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":null}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":true},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":null},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":null},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":null},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":null},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"probably","mediaSource":null},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"probably","mediaSource":null},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":null},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":null},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":null},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":null},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":null},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":null},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":null},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":null},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":null},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":null},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":null},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":null},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":null},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":null},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":null},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":null},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":null}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":true},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":true},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"","mediaSource":false},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":true},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":true},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":true},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":true},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"","mediaSource":false},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp9\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"","mediaSource":false},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"probably","mediaSource":true}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp8\\"":{"canPlay":"","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"","mediaSource":true},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"probably","mediaSource":true}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":null},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":null},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"","mediaSource":null},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"","mediaSource":null},"video/webm; codecs=\\"vp8\\"":{"canPlay":"","mediaSource":null},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"","mediaSource":null},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"","mediaSource":null},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"","mediaSource":null},"video/webm; codecs=\\"vp9\\"":{"canPlay":"","mediaSource":null},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"","mediaSource":null},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"","mediaSource":null},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":null},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":null},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":null},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":null},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":null},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":null},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":null},"video/ogg; codecs=\\"flac\\"":{"canPlay":"","mediaSource":null},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"probably","mediaSource":null}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":true},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":true},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":true},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":true},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":true},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"","mediaSource":true},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":true},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":true},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp8\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp9\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"","mediaSource":false},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"probably","mediaSource":true}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":true},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":false},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":false},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":false},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":false},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":false},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":false},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"probably","mediaSource":false},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":false},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"probably","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"probably","mediaSource":false}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"","mediaSource":false},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"probably","mediaSource":true}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":false},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":false},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":false},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":false},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":false},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":false},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"probably","mediaSource":false},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":false},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"","mediaSource":false},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":true},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"probably","mediaSource":true}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":true},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp8\\"":{"canPlay":"","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"","mediaSource":true},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"","mediaSource":false},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"probably","mediaSource":true}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":true},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"maybe","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"","mediaSource":false},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"probably","mediaSource":true}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":true},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":true},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":false},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":false},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":true},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":true},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":null},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":null},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":null},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":null},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"","mediaSource":null},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"probably","mediaSource":null},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":null},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":null},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":null},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":null},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":null},"video/webm; codecs=\\"vp9\\"":{"canPlay":"","mediaSource":null},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"","mediaSource":null},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"","mediaSource":null},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":null},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":null},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":null},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":null},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":null},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":null},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":null},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":null},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":null}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":true},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"probably","mediaSource":true},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"","mediaSource":true},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"","mediaSource":true},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":true},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"","mediaSource":true},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"","mediaSource":true},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"probably","mediaSource":true}',
        '{"video/mp4; codecs=\\"hev1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.90\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hev1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"hvc1.1.6.L93.B0\\"":{"canPlay":"","mediaSource":false},"video/mp4; codecs=\\"vp09.00.10.08\\"":{"canPlay":"probably","mediaSource":false},"video/mp4; codecs=\\"vp09.00.50.08\\"":{"canPlay":"probably","mediaSource":false},"video/mp4; codecs=\\"vp09.01.20.08.01\\"":{"canPlay":"probably","mediaSource":false},"video/mp4; codecs=\\"vp09.01.20.08.01.01.01.01.00\\"":{"canPlay":"probably","mediaSource":false},"video/mp4; codecs=\\"vp09.02.10.10.01.09.16.09.01\\"":{"canPlay":"probably","mediaSource":false},"video/mp4; codecs=\\"av01.0.08M.08\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8.0, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp8, opus\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp9\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp9, vorbis\\"":{"canPlay":"probably","mediaSource":false},"video/webm; codecs=\\"vp9, opus\\"":{"canPlay":"probably","mediaSource":false},"video/x-matroska; codecs=\\"theora\\"":{"canPlay":"","mediaSource":false},"application/x-mpegURL; codecs=\\"avc1.42E01E\\"":{"canPlay":"probably","mediaSource":false},"video/ogg; codecs=\\"dirac, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, speex\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, vorbis\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"theora, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"dirac, flac\\"":{"canPlay":"","mediaSource":false},"video/ogg; codecs=\\"flac\\"":{"canPlay":"probably","mediaSource":false},"video/3gpp; codecs=\\"mp4v.20.8, samr\\"":{"canPlay":"","mediaSource":false}']
    return random.choice(video_codecs_extendeds)


# 定义一个函数来模拟屏幕方向
def fake_screen_orientation():
    orientations = ["portrait-primary", "portrait-secondary", "landscape-primary", "landscape-secondary"]
    return random.choice(orientations)


# 定义一个函数来模拟是否启用了PDF查看器插件
def fake_pdf_viewer_enabled():
    return random.choice([True, False])


# 定义一个函数来模拟不同类型的处理器架构
def fake_platform_architecture():
    architectures = ["Win64", "x86", "x86_64"]
    return random.choice(architectures)


audio_fingerprint_list = ['124.08072766105033', '124.04651710136386', '124.0807279153014', '124.04344968475198',
                          '124.08072784824617',
                          '124.0396717004187', '35.73832903057337', '124.0807277960921', '124.08075528279005',
                          '124.08072790785081',
                          '124.08072256811283', '124.04345259929687', '124.0434496849557', '124.0434806260746',
                          '124.08072782589443',
                          '64.39679384598276', '124.0434485301812', '124.04423786447296', '124.04453790388652',
                          '124.08072786314733',
                          '124.04569787243236', '124.08072787804849', '124.04211016517365', '124.08072793765314',
                          '124.03962087413674',
                          '124.04457049137272', '124.04344884395687', '35.73833402246237', '124.0434474653739',
                          '124.04855314017914',
                          '124.04347524535842', '35.10893232002854', '124.08072787802666', '124.04048140646773',
                          '28.601430902344873',
                          '35.749968223273754', '35.74996031448245', '124.0434752900619', '124.04347657808103',
                          '124.04215029208717',
                          '124.08072781844385', '124.04369539513573', '124.04384341745754', '124.04557180271513',
                          '35.74996626004577',
                          '124.0807470110085', '124.04066697827511', '124.08072783334501', '124.40494026464876',
                          '124.0434488439787',
                          '35.7383295930922', '124.03549310178641', '124.04304748237337', '124.08075643483608',
                          '124.0437401577874',
                          '124.05001448364783', '124.08072795627959', '124.04345808873768', '124.04051324382453',
                          '124.04347527516074',
                          '124.08072796745546', '124.0431715620507']

video_codecs_extended_hash_list = ['bef03544979e61fc6c866a6ed8558293', '8aded24bf2127d1c53e0f64619143877',
                                   '6b7f58ca77347689dba1cc082f6cdb39',
                                   '415f3beb302a33db03add30f16e94f01', 'f0239c7eafe00fdb4937aae458fb2913',
                                   'ca5cb29fe3ffe62292915dcf3fffe1d1',
                                   '5648501a58d24ea22ce3773cc234e563', 'd0e44cce1aef6cb82325da367372a6c9',
                                   '5607d598c4fbe2dae6937c5e42d499af',
                                   'cb2c967d0cd625019556b39c63f7d435', '7ea44e9c348ffc10643a3b03876cbb5f',
                                   '69a19327d4a0aea8a700f1d0f32ad106',
                                   'ca9c00558d795e40768970cf2b0d4422', '78469332f8a1d8e4dddb08bb6f6b8413',
                                   '00d7d06cb48804b857cbdf0fdaa082cd',
                                   '2c0427743501d32adcd3ef8ff9bf134d', '89f80f70718ecdafe0a881f4b31d1aa8',
                                   '26c510713a940b647aba51de63d5e6f7',
                                   '18f9253bb6df8c476ff425f19bc1a304', '67b509547efe3423d32a3a70a2553c16',
                                   '01fa6d6eebb07be315e0a107455b0f37',
                                   'c9c9e7ddac48b1e637b30c59c76f7f30', '197d4013d0ea2417048fc18da130f580',
                                   '996d499199483186e5faed9dd3f648fb',
                                   '8f1feaf56441cf89fb1c5d4adccb6b63', '4df7a7e37de1c8314a2a64851b25fdad',
                                   'cf5d14c05ee3a829834d94c9436bd774',
                                   'dced6698c96ade4125003fd84a33883d', 'e21eb9ea2d92fb2fa231d09ec1115e32',
                                   '6aaa9ba84ae44934e123a341c29fe8de',
                                   'e931058be75998f577f0a20ed658f114', 'b489ea588756e8a430af84ddfb5bc954',
                                   '355432e2bb2644728ba876fb1fe3237f',
                                   'b55d0e65c00b240e47ff5b39e3c5c8d3', '2bd35d9cede66bd64d2ef015473b6e89',
                                   '700881bf5d79fe76b11968d8fe497460',
                                   '87a2a24f6e708312c549ed591b623acd', '233f3071eaec5e0b12fe32b3580587e3',
                                   '860df88c1903a4e3930122c4dec33a52']

math_fingerprint_list = ['7808ee4c88973bb281fb11290c1c856d', 'e4889aec3d9e3cdc6602c187bc80a578',
                         '3b2ff195f341257a6a2abbc122f4ae67',
                         'a4a0969d7190fb9813b136b745c5165e', '60e58b3e935648626aae79b083054cdb',
                         '0ac0d5bc7143a8c3dfe7fe323742f45c',
                         '25425eecc5283a6e381112c9448f9212', '3a545b4c686955d78950295cca1d3e7b',
                         'd1f0d718dc35469b254ef63603d70944',
                         '187f89900440278259358be82768544a', 'be2a25cdc137da78514daf1c61b6afab',
                         '053f3ee2d6545dfb4bbf2c280f551c72']

supported_math_functions_list = ['e9dd4fafb44ee489f48f7c93d0f48163', 'afad9aebfa1a08d54b39f540d0c002f1',
                                 '1f065bfb481d04c2f047bac7df57b8ac']

speech_default_voice_list = ['English United States || en_US', 'Microsoft Ayumi - Japanese (Japan) || ja-JP',
                             'Google Deutsch || de-DE',
                             'Tingting || zh-CN', 'Zuzana || cs-CZ', '英文 英國 || en_GB',
                             'Microsoft David - English (United States) || en-US',
                             'Microsoft Adri Online (Natural) - Afrikaans (South Africa) || af-ZA',
                             '保加利亞文 保加利亞 || bg_BG',
                             'Kyoko || ja-JP', 'Microsoft Irina - Russian (Russia) || ru-RU', '婷婷 || zh-CN',
                             'Meijia || zh-TW',
                             'Tom || en-US', 'Tünde || hu-HU', 'Microsoft George - English (United Kingdom) || en-GB',
                             'Bulgarian Bulgaria || bg_BG', '保加利亚语 保加利亚 || bg_BG', 'German Germany || de_DE',
                             'Microsoft Huihui - Chinese (Simplified, PRC) || zh-CN',
                             'Microsoft Tolga - Turkish (Turkey) || tr-TR',
                             'болгарский Болгария || bg_BG',
                             'Microsoft Kangkang Mobile - Chinese (Simplified, PRC) || zh-CN',
                             'Mei-Jia || zh-TW', 'Microsoft Huihui Mobile - Chinese (Simplified, PRC) || zh-CN',
                             'Microsoft Huihui Desktop - Chinese (Simplified) || zh-CN', 'Alex || en-US',
                             'Daria || bg-BG',
                             'Samantha || en-US', 'Ting-Ting || zh-CN', '美嘉 || zh-TW',
                             'Microsoft Heera - English (India) || en-IN',
                             'Microsoft Lili - Chinese (China) || zh-CN', 'Sin-ji || zh-HK',
                             'Microsoft Hanhan - Chinese (Traditional, Taiwan) || zh-TW',
                             'انگلیسی ایالات متحده || en_US',
                             'Ting-Ting || zh-Hans', 'Aaron || en-US', 'Microsoft Heami - Korean (Korean) || ko-KR',
                             '英语 美国 || en_US',
                             'Microsoft Aria Online (Natural) - English (United States) || en-US',
                             'Microsoft Zira Desktop - English (United States) || en-US', 'Carmit || he-IL']

speech_voices_hash_list = ['d20444594b9ceaa29fe999fcc8fe1a49', 'bcaeeb7aa769856bf6230bb4f0678e51',
                           '61cd8caa7810cce6f24773b4bf49804d',
                           '6813a00ef397a9899d04113dea91e265', 'ec9713c8fd8484df043cbcf867b469c1',
                           '3715cd89b0e1ba721b72915b9d7cf5bf',
                           'b096798bbdbf3984a4a2bb6ac1592370', '8ea055c31a64f2efc6717e68e4c10cb9',
                           'e4f0c6b073f8c705741f3fd434d9a38a',
                           '20374c52d9a0c931f9df2434f08b827e', 'b2c0cc53e9551925eaca20a1ae4a83b4',
                           '461450cfe79fc7955e18b52eb08f2e7d',
                           '85862584642275d9451d9d35c44236f6', '73ad71db4552328df27e3d2c113ddeb2',
                           '117650b025ddfbcc66259fd79222dddd',
                           'f3798f2ec73243f4b00a5eb51de7c4f8', 'a90f45a692df0a7ff21fc3f2ae06065a',
                           'beaa329e0c0a9666cde66b9b54a58874',
                           '08c31d5031ebc71b78e5ba4600428e10', '4ee40e20982010a2cad536d73ec6e531',
                           '64f4a13e41396ac21e53a1f674631b7e',
                           'ca2bfa0ac19a802a5aba0ced0cf353b2', 'cc0f7013ff749269e5793e3c07db7c93',
                           'be88f672061decbf48b912828e6a443c',
                           'e16be4f4857f29b99dce3bfba1753808', 'cb4dce4acb2c97e02b9c7363a17c6aab',
                           '83caf5bfb0896f21aaa92327aca567ae',
                           'f0b7baf8fcc35823f5bdfd8d548aa62e', 'e25e1be18b7b18281a7df1985a025c3e',
                           'f496e50f79205be7125b5fc288b900a9',
                           'd3300f33c956c0991838012203d2cf0f', '464caba1ac3028586e6804efae2a9754',
                           '9d06b98dccda5dc55f883584b0f670c5',
                           '9e23f37b63ae4c07feb5ec203a33cfb8', 'aa0d5453319cc975c6925aa463d30d53',
                           'd8dba93072f82384755a4dcd49c89aa6',
                           'b52ced3f9b8ef74d0c717a0b90091706', '19f77a385feea0cdb895f0f84a2933e3',
                           '6a1f59c514f583dd857656978ea28ba3',
                           'ce0f6567d86cae6725f533b82db782d8', '6493d95e557b95a2b5a890649596d06c',
                           '78f1436527602dc5da136528c0c7edc1',
                           '8bcab812f19b626dcf61f5ec489c5dc0', 'f6a7962bcb8edc3eb8615c24f00640ec',
                           'f410e9b1c780bb22619dbe5cc57a467d',
                           '1a2659eef7f9aa244c4ddb2c42031f2b', '7efb3563da049101521bf1d0c3c8db92',
                           '16464a85ad4deab2bdaea4cef629214d',
                           '5d5a597e70ae60aa46be468b87ff210d', '4aaf4b29d3edaa8041ac54036a2b0056',
                           '69f3b70f92deb65b19f78fbf6f410021',
                           '653f5922c5d31882c1f0f7479b8efc89', '6f3aa968c0d68571587d9805bdb53c15',
                           'ef0406d3f0175cd86fea99090a7a7cf0',
                           '8ea4af21e256614428ba1f2ad810f43e', 'ae1b7ac2d93748e6a2dbf8341e513bef',
                           '47b86c6c57806d2ab8ced17143d82ff0',
                           '273ea403f642f9905b251e7ea1f4e078', 'c6db690821e47a5128572d07a34f9868',
                           '91d385672eedb8051e5d2a62dd079f3d',
                           '59777646768dacd5125b812317147aff', '09c3e0adf9317413d8c8e7eac960b8f4',
                           'f0aaf89142da20adf6ebd064fb18e4d7',
                           'acbc2098cb978c5efa955c60dd0e97b7', 'b24bd471a2b801a80c0e3592b0c0c362',
                           '0570e65a5e50fdee6b4a7e567020e36f',
                           'c322126db86b6bd592d5d71d78546918', 'd592348aa39f7779e02803f6d57e1cce',
                           'def535747ab849d43906f955378d49de',
                           'bd962d42dcd08bd4818d2106f6b05f0a', 'b348d98debc600167431189ada823967',
                           '8b8ff3376cac8714542e5ee2e5ae5e09',
                           '38ed9d0471e63e4d8955234dad94584d', '87cffa024a3be4b717c2b7e1e4f55109',
                           'a0c90ca98043f0489c1e731e233b937e',
                           '27e3225e3fe0e60dfefd0854c990fcdd', '33c8c01b2b63ed783cf9e91e7900abaa',
                           '2958a838919994d93e692d21a8984f86',
                           'a065dc24844fc434e52e7902ef66bf85', 'aa0906633b27e946dbc8f23a9b6acf20',
                           'b313d6f8fb7ff5416f05ae8bc552c941',
                           'c61db31c0469f42c8d39a7b314db4215', '3fd29562e728fd8e8bbfe427b17ad10e',
                           '28bba4c488fd8940c97a928e9443ee17',
                           '1aac1960a89f1e79c1d2a560d73912eb', 'b2b2840ac58294edb1b0d41650f14ec1',
                           '9357556c0445d10ea0fb1d5d1e670c60',
                           'c23f0db37c47b3e4535fe4cb0deb91b5', 'fffe1dcb5350d0074730ea3d0d12a8b1',
                           '3001ac245d4f094510bc66af5ff21d5c',
                           '4a3a3308a0529b112920b73a20b55976', '25795190d088c1864914e3f1e795e95d',
                           '00d269b3993bb461c75d0158fb7844ba',
                           '7905cccf3c591948f965df8aa24a1d8b', '28a831d49a3ddd58733b30fec741722b',
                           '093c632008f2eb7737830c884f57953b',
                           'cf4f0ac048ce5d0935257c5821afdc3b', '1a7fb1dc2495d227a6971b99a653cb12',
                           '489ab45ea2e1610d419033f6ac71639c',
                           'b4a99c599f636e5381f7af4a85851bf3', 'c2e6577f8f08b2961a25db506c0c4ce8',
                           '68e28e73698c888f55a4494315b13a74',
                           '0ff07e4f35fb872c674a251e49988ea1', '24ed5a8736a30c03235b0f9c99d303cc',
                           'b7a57b823ed28a94639a5523290d52a2',
                           'a8311561965d7433dbb44b64f3dddb41', 'fff37061b65bab9690a7e6c75316ecc3',
                           'e654f40320a8df2052fa37043a3ca4fa',
                           '9ce030bd9e278578959c83b7368ac21d', '57bb26c25673b2756e2320733a90673f',
                           '567e4676e3fb80780ad319247c0ec039',
                           '1e9fab81d99e3dc0cf8624138073c4d1', 'a73fb7afa9724c0da44c79bff0857eef',
                           'b3af8c42a073188ba0849006e37ca052',
                           'dd193e1a7ec18e9c36618e30b910a8f8', '2327c6a6bd0bdf207e8956094e968c6b',
                           'd3cc497dcce7a808aabd25ea20b92034',
                           '08da5d115bca131aee65fbb4891da5ca', '15544006e18c141021c27e07d53708cb',
                           'd716838aaaf6d689be77ba9bc7341cb8',
                           '373bcb907315e4b8c58215050584c2d2', '35aa3c94be15a9a2b7b3384abef9a866',
                           'cbe5ee2755ada90aa753bffd302134f3',
                           '58f2fbed42e16ca3bd627dc1deb6b4e1', '17404a50200c00cc1f1723f9131610e4',
                           '2bce19d312a9798479d7929810311f81',
                           '8ca3f2d57ebc46d29d60548a90a2e932', '6d656c718fe2067db573aa2c92762cfd',
                           '6563c83f229d8c8021ce574261481643',
                           'db256e3bd8b20fe93feda2737f1535ce', 'a36b8ec352d0d9b51277d37cbc5b83b0',
                           'ce2c1c510a1b7bd78f32a83323d2ccda',
                           '5b8f229972a64fb69f7fcd885253afa1', '87f679553cef8359171e2d3d1661177d',
                           'e9db3afbe0fa54bf2a03a91024d87128',
                           'd706032f7e991d942240d63b948aa932', '4a6e6a048491eac77a0ea977599de68b',
                           '227280897d60b5a85c14973a88d1cea2',
                           'a8e341c6a4bf197b649d5536898b4eab', 'a54dff00325c30833cd22af207a73ed0',
                           'b5377075d2b8a6eb91e59bb9a3e8517d',
                           'e58a9f8bd680b196e831b95f32d8c711', '34118aa273ed11279b9558d8f30720ff',
                           '76e52c5516f8ca7d1881344e7629a9a9',
                           '5f9105536fd7e452ce28448d57f77f93', 'a9759508eec708f096c4bcfa6f92d9eb',
                           '0a1c1f90ed33f7c3ff057c5b1d87cb1f',
                           '606af5bad7fbede97d4b7d5487f23849', 'f91201dc85d490e4d5db1216c2e949d9',
                           'f859c02fd2bc0afc6982ad7b705a7b4c',
                           'ce1355555d7f2d4fd7761b2d0852254f', '84d9604d0a627f1b4a45fd54864625b8',
                           '96753c7678316b1ab46f3cf2ed6040bf',
                           '7175df034a3cac88f5c8175d1268894b', 'ad40ad4ef5775e5165a0fdb8f50418cf',
                           '6513b15e5fe9ff98d5704bc45b387235',
                           '151fba5328f03110f5bf58753f20296f', 'c086de0cdc5abee9e1479c09bc99ca5c',
                           '5c112548739e3f4eade9b1e213ba80a1',
                           '5129df13abf38e5719560b61fab8109f', 'fc30ce9a0abecfee0abaca8ae21c866d',
                           'ded126cc29315adb46fafadfeb3891ee',
                           '8d7dba4fa536f48ba482725c634ccece', 'a9a325879f491ef5e757801de9e7a126',
                           '89d9bb615bd01838450cc4e128943557',
                           '02348de71b242477ededa6333fb48cb3', 'd5fd33f4eb8bf0a0d1b29f0831b93c52',
                           '69ed8fec0bf9ef8c4f612b4270416dbd',
                           '67803d5abf81ba6bb365f3270e0827f0', '7abb6f8f2dc15663c79ab8abce8990d7',
                           '43a58b4c12a122859dccf0f03ea847f9',
                           'ac7140396bbaab611adb23bed9488125']


def convert_json_to_dict(json_data):
    result_dict = {}
    for item in json_data:
        key = item.get('key')
        value = item.get('value')
        result_dict[key] = value
    return result_dict


def convert_dict_to_json(original_dict):
    json_data = [{"key": key, "value": value} for key, value in original_dict.items()]
    return json_data


def get_enhanced_fp(fp, ua, sec_ch_ua):
    with open("./src/enhanced_fp.json", "r") as f:
        enhanced_fp_kv = json.load(f)
    enhanced_fp = convert_json_to_dict(enhanced_fp_kv)
    enhanced_fp['webgl_extensions'] = ";".join(
        random.sample(enhanced_fp['webgl_extensions'].split(";"), k=random.randint(15, 28)))
    enhanced_fp["webgl_extensions_hash"] = x64hash128(enhanced_fp['webgl_extensions'], 0)
    enhanced_fp["screen_pixel_depth"] = int(fp["D"])
    enhanced_fp["navigator_languages"] = fp["L"]
    enhanced_fp["window_outer_height"] = int(fp["S"].split(",")[1])
    enhanced_fp["window_outer_width"] = int(fp["S"].split(",")[0])
    enhanced_fp["window_inner_height"] = 0
    enhanced_fp["window_inner_width"] = 0
    enhanced_fp["browser_detection_firefox"] = bool(re.search(r'Firefox/\d+', ua))
    enhanced_fp["browser_detection_brave"] = bool(re.search(r'Brave/\d+', ua))
    enhanced_fp["media_query_dark_mode"] = bool(random.random() > 0.9)

    enhanced_fp["css_media_queries"] = random.choice([0, 1])
    enhanced_fp["css_color_gamut"] = random.choice(["p3", "srgb"])

    enhanced_fp["webgl_renderer"] = fake_webgl_renderer()
    enhanced_fp["webgl_vendor"] = fake_webgl_vendor()
    enhanced_fp["webgl_shading_language_version"] = fake_webgl_shading_language_version()
    enhanced_fp["webgl_aliased_line_width_range"] = fake_webgl_aliased_line_width_range()
    enhanced_fp["webgl_max_params"] = fake_webgl_max_params()
    enhanced_fp["webgl_max_viewport_dims"] = fake_webgl_max_viewport_dims()
    enhanced_fp["webgl_unmasked_vendor"] = fake_webgl_unmasked_vendor()
    enhanced_fp["webgl_unmasked_renderer"] = fake_webgl_unmasked_renderer()
    enhanced_fp["webgl_vsf_params"] = fake_webgl_vsf_params()
    enhanced_fp["webgl_vsi_params"] = fake_webgl_vsi_params()
    enhanced_fp["webgl_fsf_params"] = fake_webgl_fsf_params()
    enhanced_fp["webgl_fsi_params"] = fake_webgl_fsi_params()
    enhanced_fp["webgl_hash_webgl"] = x64hash128(','.join(
        value for key, value in enhanced_fp.items() if key.startswith('webgl_') and key != 'webgl_hash_webgl'), 0)

    enhanced_fp["navigator_pdf_viewer_enabled"] = fake_pdf_viewer_enabled()
    enhanced_fp["navigator_device_memory"] = 8
    enhanced_fp["navigator_battery_charging"] = fake_battery_charging()
    enhanced_fp["navigator_connection_downlink"] = random.choice(navigator_connection_downlink_list)
    enhanced_fp["network_info_rtt"] = random.choice(network_info_rtt_list)
    enhanced_fp["user_agent_data_brands"] = ",".join(re.findall(r'(?<=")[^"]*(?=";)', sec_ch_ua))

    enhanced_fp["audio_codecs"] = fake_audio_codecs_support()
    enhanced_fp["audio_fingerprint"] = random.choice(audio_fingerprint_list)
    enhanced_fp["video_codecs"] = fake_video_codecs_support()
    enhanced_fp["video_codecs_extended"] = fake_video_codecs_extended()
    enhanced_fp["video_codecs_extended_hash"] = random.choice(video_codecs_extended_hash_list)
    enhanced_fp["math_fingerprint"] = random.choice(math_fingerprint_list)
    enhanced_fp["supported_math_functions"] = random.choice(supported_math_functions_list)
    enhanced_fp["speech_default_voice"] = random.choice(speech_default_voice_list)
    enhanced_fp["speech_voices_hash"] = random.choice(speech_voices_hash_list)
    enhanced_fp["screen_orientation"] = fake_screen_orientation()

    enhanced_fp["4b4b269e68"] = str(uuid.uuid4())
    enhanced_fp["6a62b2a558"] = enforcement_hash
    enhanced_fp["1l2l5234ar2"] = str(int(time.time() * 1000)) + '?'

    if "Firefox" in ua:
        enhanced_fp["user_agent_data_brands"] = None
        enhanced_fp["user_agent_data_mobile"] = None
        enhanced_fp["navigator_connection_downlink"] = None
        enhanced_fp["network_info_rtt"] = None
        enhanced_fp["network_info_save_data"] = None
        enhanced_fp["navigator_device_memory"] = None
        enhanced_fp["browser_api_checks"] = [
            "permission_status: true",
            "eye_dropper: false",
            "audio_data: false",
            "writable_stream: true",
            "css_style_rule: true",
            "navigator_ua: false",
            "barcode_detector: false",
            "display_names: true",
            "contacts_manager: false",
            "svg_discard_element: false",
            "usb: NA",
            "media_device: defined",
            "playback_quality: true"
        ]
        enhanced_fp["browser_object_checks"] = None
        enhanced_fp["navigator_battery_charging"] = None
        enhanced_fp["media_device_kinds"] = None
        enhanced_fp["media_devices_hash"] = None
        enhanced_fp["speech_default_voice"] = None

    enhanced_fp_kv = convert_dict_to_json(enhanced_fp)

    return enhanced_fp_kv


def edit_enhanced_fp(decrypted_bda, method):
    decrypted_bda_dict = convert_json_to_dict(decrypted_bda)
    enhanced_fp = convert_json_to_dict(decrypted_bda_dict["enhanced_fp"])

    fun_options = FunCaptchaOptions(method=method)
    enhanced_fp.update(fun_options.options)

    decrypted_bda_dict["enhanced_fp"] = convert_dict_to_json(enhanced_fp)
    decrypted_bda = convert_dict_to_json(decrypted_bda_dict)
    return decrypted_bda
