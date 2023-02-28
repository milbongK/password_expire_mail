# password_expire_mail


cat /etc/passwd
admin:x:0:1000:milbong@test.com:/home/admin:/bin/bash
apache:x:48:48:Apache:/usr/share/httpd:/sbin/nologin

위와 같이 passwd 내에 계정 설명 부분에 패스워드 만료 알람을 받고자 하는 메일 계정을 써준다.

이후, 크론탭을 이용하여 해당 py 파일을 매일 정해진 시간이 실행하면 오늘 날짜와, 계정 패스워드 마지막 변경일자를 비교하여 조건 만족 시, 
