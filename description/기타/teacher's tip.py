'''
강사님은 뭐든 먹을 수 있다.
맛집: 엄용백 돼지국밥
지론 
1. 여자가 많다 : 가격은 비싸나 맛있는 지는 모르겠다
2. 남자가 많다 : 가격은 싸나 맛있는 지는 모르겠다
3. 할아버지 할머니 있는 집이 제일 맛있다.
'''
# 파이썬 한글화 : 시스템 환경 변수 편집 들어가서 처리 --> 고급 -> TJ에 대한 변수 PythonIOEncoding에 utf-8 추가 되어있나 확인.
# IO = Input, Output
# 시스템 변수 : 현재 연결 되어 있는 데스크톱 전체에 적용하는 설정
# TJ에 대한 사용자 변수 : 컴퓨터에서 특정 계정에만 적용하는 설정
# 시스템 환경 변수하는 곳은 개발자나 컴퓨터를 사용하는 편리하게 만들기 위한 공간
# 사용자 환경 변수 - 실수 해도 나의 계정만 문제가 생기기 때문에 복구 쉬움
# 시스템 환경 변수 - 실수하면 윈도우 기능이 먹통 될 수 있다.
# 환경 변수를 설정하는 것은 미리 컴퓨터에게 이 폴더는 자주 사용하는 폴더이니 기억을 했으면 좋겠어 등록하는 것임.

'''
PS C:\Users\TJ\Desktop\python-workspace> pip install gTTS playsound
Collecting gTTS
  Obtaining dependency information for gTTS from https://files.pythonhosted.org/packages/e3/6c/8b8b1fdcaee7e268536f1bb00183a5894627726b54a9ddc6fc9909888447/gTTS-2.5.4-py3-none-any.whl.metadata
  Downloading gTTS-2.5.4-py3-none-any.whl.metadata (4.1 kB)
Collecting playsound
  Downloading playsound-1.3.0.tar.gz (7.7 kB)
  Installing build dependencies ... done
  Getting requirements to build wheel ... error
  error: subprocess-exited-with-error

  × Getting requirements to build wheel did not run successfully.
  │ exit code: 1
  ╰─> [28 lines of output]
      Traceback (most recent call last):
        File "C:\Users\TJ\AppData\Local\Programs\Python\Python312\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\_in_process.py", line 353, in <module>
          main()
        File "C:\Users\TJ\AppData\Local\Programs\Python\Python312\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\_in_process.py", line 335, in main 
          json_out['return_val'] = hook(**hook_input['kwargs'])
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File "C:\Users\TJ\AppData\Local\Programs\Python\Python312\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\_in_process.py", line 118, in get_requires_for_build_wheel
          return hook(config_settings)
                 ^^^^^^^^^^^^^^^^^^^^^
        File "C:\Users\TJ\AppData\Local\Temp\pip-build-env-10hvdke6\overlay\Lib\site-packages\setuptools\build_meta.py", line 331, in get_requires_for_build_wheel
          return self._get_build_requires(config_settings, requirements=[])
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File "C:\Users\TJ\AppData\Local\Temp\pip-build-env-10hvdke6\overlay\Lib\site-packages\setuptools\build_meta.py", line 301, in _get_build_requires      
          self.run_setup()
        File "C:\Users\TJ\AppData\Local\Temp\pip-build-env-10hvdke6\overlay\Lib\site-packages\setuptools\build_meta.py", line 512, in run_setup
          super().run_setup(setup_script=setup_script)
        File "C:\Users\TJ\AppData\Local\Temp\pip-build-env-10hvdke6\overlay\Lib\site-packages\setuptools\build_meta.py", line 317, in run_setup
          exec(code, locals())
        File "<string>", line 6, in <module>
        File "C:\Users\TJ\AppData\Local\Programs\Python\Python312\Lib\inspect.py", line 1282, in getsource
          lines, lnum = getsourcelines(object)
                        ^^^^^^^^^^^^^^^^^^^^^^
        File "C:\Users\TJ\AppData\Local\Programs\Python\Python312\Lib\inspect.py", line 1264, in getsourcelines
          lines, lnum = findsource(object)
                        ^^^^^^^^^^^^^^^^^^
        File "C:\Users\TJ\AppData\Local\Programs\Python\Python312\Lib\inspect.py", line 1093, in findsource
          raise OSError('could not get source code')
      OSError: could not get source code
      [end of output]

  note: This error originates from a subprocess, and is likely not a problem with pip.
error: subprocess-exited-with-error
× Getting requirements to build wheel did not run successfully.
│ exit code: 1
╰─> See above for output.

note: This error originates from a subprocess, and is likely not a problem with pip.

[notice] A new release of pip is available: 23.2.1 -> 25.3
[notice] To update, run: python.exe -m pip install --upgrade pip
PS C:\Users\TJ\Desktop\python-workspace> python.exe -m pip install --upgrade pip
Requirement already satisfied: pip in c:\users\tj\appdata\local\programs\python\python312\lib\site-packages (23.2.1)
Collecting pip
  Obtaining dependency information for pip from https://files.pythonhosted.org/packages/44/3c/d717024885424591d5376220b5e836c2d5293ce2011523c9de23ff7bf068/pip-25.3-py3-none-any.whl.metadata
Downloading pip-25.3-py3-none-any.whl (1.8 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 8.1 MB/s eta 0:00:00
Installing collected packages: pip
  Attempting uninstall: pip
    Found existing installation: pip 23.2.1
    Uninstalling pip-23.2.1:
      Successfully uninstalled pip-23.2.1
Successfully installed pip-25.3
PS C:\Users\TJ\Desktop\python-workspace> pip install gTTS playsound
Collecting gTTS
  Downloading gTTS-2.5.4-py3-none-any.whl.metadata (4.1 kB)
Collecting playsound
  Downloading playsound-1.3.0.tar.gz (7.7 kB)
  Installing build dependencies ... done
  Getting requirements to build wheel ... error
  error: subprocess-exited-with-error

  × Getting requirements to build wheel did not run successfully.
  │ exit code: 1
  ╰─> [28 lines of output]
      Traceback (most recent call last):
        File "C:\Users\TJ\AppData\Local\Programs\Python\Python312\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\_in_process.py", line 389, in <module>
          main()
        File "C:\Users\TJ\AppData\Local\Programs\Python\Python312\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\_in_process.py", line 373, in main 
          json_out["return_val"] = hook(**hook_input["kwargs"])
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File "C:\Users\TJ\AppData\Local\Programs\Python\Python312\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\_in_process.py", line 143, in get_requires_for_build_wheel
          return hook(config_settings)
                 ^^^^^^^^^^^^^^^^^^^^^
        File "C:\Users\TJ\AppData\Local\Temp\pip-build-env-6hs7h312\overlay\Lib\site-packages\setuptools\build_meta.py", line 331, in get_requires_for_build_wheel
          return self._get_build_requires(config_settings, requirements=[])
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File "C:\Users\TJ\AppData\Local\Temp\pip-build-env-6hs7h312\overlay\Lib\site-packages\setuptools\build_meta.py", line 301, in _get_build_requires      
          self.run_setup()
        File "C:\Users\TJ\AppData\Local\Temp\pip-build-env-6hs7h312\overlay\Lib\site-packages\setuptools\build_meta.py", line 512, in run_setup
          super().run_setup(setup_script=setup_script)
        File "C:\Users\TJ\AppData\Local\Temp\pip-build-env-6hs7h312\overlay\Lib\site-packages\setuptools\build_meta.py", line 317, in run_setup
          exec(code, locals())
        File "<string>", line 6, in <module>
        File "C:\Users\TJ\AppData\Local\Programs\Python\Python312\Lib\inspect.py", line 1282, in getsource
          lines, lnum = getsourcelines(object)
                        ^^^^^^^^^^^^^^^^^^^^^^
        File "C:\Users\TJ\AppData\Local\Programs\Python\Python312\Lib\inspect.py", line 1264, in getsourcelines
          lines, lnum = findsource(object)
                        ^^^^^^^^^^^^^^^^^^
        File "C:\Users\TJ\AppData\Local\Programs\Python\Python312\Lib\inspect.py", line 1093, in findsource
          raise OSError('could not get source code')
      OSError: could not get source code
      [end of output]

  note: This error originates from a subprocess, and is likely not a problem with pip.
ERROR: Failed to build 'playsound' when getting requirements to build wheel
PS C:\Users\TJ\Desktop\python-workspace> 
'''