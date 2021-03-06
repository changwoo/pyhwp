pyhwp: hwp 파일 포맷 파서
=========================

소개
----

HWP 5.0 파일(.hwp)을 분석하는 파이썬 프로그램입니다. HWP 5.0 복합 파일에 포함된
내부 스트림들을 분리해 내거나, 레코드 데이터 구조를 덤프/파싱할 수 있습니다.

현재 다음의 것이 가능합니다.

1. HWP 5.0 복합파일(Compound File)로부터 각 스트림을 압축된/압축해제된 형태로 
   읽어내기
2. DocInfo, BodyText/SectionX 등의 레코드 구조 스트림들을 레코드 단위로 잘라 
   읽어내기
3. 레코드 구조를 XML로 출력하기
4. HWP 파일을 XML로 변환하기

각각의 단계에 대응하는 다음 실행파일이 존재합니다:

		hwp5file <hwp파일이름> [<스트림 파일>]
		hwp5rec <hwp파일이름> <레코드 스트림 파일> [<덤프할 레코드 범위>]
		hwp5bin <hwp파일이름> <레코드 스트림 파일>
		hwp5xml <hwp파일이름>

또한 다음의 파일 형식으로 낮은 품질의 변환이 가능합니다. (libxslt의 xsltproc 
필요)

		hwp5txt <hwp파일이름>
		hwp5html <hwp파일이름>
		hwp5odt <hwp파일이름>

프로젝트 호스팅
---------------

  http://github.com/mete0r/pyhwp

요구사양
--------

 - python 2.5.4 이상
 - xsltproc (hwp5odt, hwp5html, hwp5odt)

설치방법
--------

	git clone git://github.com/mete0r/pyhwp.git
	cd pyhwp
	python bootstrap.py
	bin/buildout

사용방법
--------

### 1) hwp5file

HWP 5.0 복합파일에 포함된 스트림 파일 목록을 확인하고, 각각을 표준 출력으로 
덤프할 수 있습니다.

사용법:

		hwp5file <hwp파일이름> [<스트림 파일>]

`<스트림 파일>`을 생략할 경우, 스트림 파일 목록을 출력합니다.

예: sample.hwp 파일의 스트림 목록을 출력

		hwp5file sample.hwp

`<스트림 파일>`에 스트림 파일의 상대 경로를 명시할 경우, 그 스트림을 출력합니다.
압축된 스트림은 압축된 그대로 출력합니다.

예: sample.hwp 파일의 `DocInfo` 스트림을 출력

		hwp5file sample.hwp DocInfo > docinfo.z

예: sample.hwp 파일에 첨부된 `BinData/BIN0001.JPG`를 출력

		hwp5file sample.hwp BinData/BIN0001.JPG > BIN0001.JPG.z

`<스트림 파일>`에 다음의 이름을 입력하면, 상응하는 스트림의 압축이 해제되어 출력됩니다:

		preview_text : 	PrvText를 압축 해제하여 출력
		preview_image : PrvImage를 압축 해제하여 출력
		docinfo : DocInfo를 압축 해제하여 출력
		bodytext <index> : BodyText/Section<index>를 압축 해제하여 출력
		bindata <filename> : BIN/<filename>을 압축해제하여 출력


예: `PrvText`(미리보기 텍스트)를 출력

		hwp5file sample.hwp preview_text

예: `PrvImage`(미리보기 이미지)를 출력

		hwp5file sample.hwp preview_image > preview_image.gif

예: `DocInfo` 레코드 구조 스트림을 압축 해제하여 출력

		hwp5file sample.hwp docinfo > docinfo.bin

예: `BodyText/Section0` 레코드 구조 스트림을 압축 해제하여 출력

		hwp5file sample.hwp bodytext 0 > bodytext0.bin

예: sample.hwp 파일에 첨부된 `BinData/BIN0001.JPG`를 압축 해제하여 출력

		hwp5file sample.hwp bindata BIN0001.JPG > bin0001.jpg

### 2) hwp5rec

레코드 구조 스트림 (`DocInfo`, `BodyText/Section<number>` 등)을 트리 형태로 
덤프할 수 있습니다.

사용법:

		hwp5rec <hwp파일이름> <레코드 스트림 파일> [<덤프할 레코드 범위>]

예: `DocInfo` 레코드 구조 스트림을 출력합니다.

		hwp5rec sample.hwp docinfo

예: `BodyText/Section0` 레코드 구조 스트림을 출력합니다.

		hwp5rec sample.hwp bodytext/0

예: `BodyText/Section0`레코드 구조 스트림의 27번째 레코드를 출력합니다.

		hwp5rec sample.hwp bodytext/0 26

예: `BodyText/Section0`레코드 구조 스트림의 27~29번째 레코드를 출력합니다.

		hwp5rec sample.hwp bodytext/0 26:29

### 3) hwp5bin

HWP 5.0 파일의 레코드 구조 스트림을 Paragraph 등 데이터 모델로 파싱, JSON 파일로 
변환해서 출력합니다.

사용법:

		hwp5bin <hwp파일이름> <레코드 스트림 파일>

예:

		hwp5bin sample.hwp docinfo > docinfo.models.json
		hwp5bin sample.hwp bodytext/0 > bodytext0.models.json

### 4) hwp5xml

HWP 5.0 파일을 XML 파일로 변환합니다. 첨부된 이미지 등은 포함되지 않으며, 
DocInfo 스트림과 BodyText 스트림들만이 변환됩니다.

(출력 XML의 형식은 pyhwp에서 임시로 정의한 것으로, 현재 계속 변경 중입니다.
pyhwp가 어느 정도 성숙하면 XML 정의를 확정할 계획입니다.)

사용법:

		hwp5xml <hwp파일이름>

예:

		hwp5xml sample.hwp > sample.xml

기여자
------
   메인테이너: mete0r_kr @twitter

사용조건
--------
pyhwp는 [GNU Affero General Public License v3.0](http://github.com/mete0r/pyhwp/raw/master/pyhwp/LICENSE)의
사용 조건에 따라 제공됩니다.

기타
----
pyhwp는 [(주)한글과컴퓨터](http://www.hancom.co.kr)의 한/글 문서파일(.hwp) 공개 문서를 참고하여 개발하였습니다.
