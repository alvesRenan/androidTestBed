##### COMANDOS PARA O ADB #####

# Inicia o ADB
ADB_START = "adb devices"

# Mata o processo do ADB
ADB_KILL = "adb kill-server ; adb start-server > /dev/null "

# Lista com os dispositivos conectados
# saida exemplo:
# 	emulator-5570
LIST = "adb devices | awk 'NR>1 { print($1) }'"

# Instala a aplicacao em dispositivo
# exemplo: adb -s emulator-5070 install -rt App.apk
INSTALL_APP = "adb -s emulator-%s install -rt %s"

# Inicia a activity principal da aplicacao
# Exemplo: adb -s emulator-5070 shell am start -S br.ufc.great.matrixoperation/.MainActivity
ACTIVITY = "adb -s emulator-%s shell am start -S %s"

# Inicia a activity passando o IP do cloudlet
# Exemplo: adb -s emulator-5070 shell am start -n br.ufc.great.matrixoperation/.MainActivity --es "cloudlet" "172.18.0.2"
SET_CLOUDLET = "adb -s emulator-%s shell am start -n %s --es 'cloudlet' '%s'"

# Executa uma activity da aplicacao em um dispositivo passando o IP da cloudlet
# exemplo: adb -s emulator-5070 shell am start -n br.ufc.great.matrixoperation/.MainActivity --es "cloudlet" "172.18.0.2" --es "operation" "mul" --ei "size" 500
EXEC = "adb -s emulator-%s shell am start -n %s --es 'cloudlet' '%s' %s"

# Coleta os dados de execucao do logcat e salva em um arquivo com o mesmo nome do container
# Exemplo: adb -s emulator-5070 shell logcat -t | grep DebugRpc > diretorio/file.txt
RESULTS = "adb -s emulator-%s shell logcat -d | grep DebugRpc > %s/%s"

# Limpa o logcat do dispositivo
# Exemplo: adb -s emulator-5070 shell logcat -c
CLEAR_LOG = "adb -s emulator-%s shell logcat -c"

###################################


##### COMANDOS PARA CONTAINERS #####

# Retorna o IP de um container dado o seu nome
# exemplo: docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' android-01
GET_IP = "docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' %s"

# Inicia o emulador com a configuracao de rede indicada em um container com estado PARADO ou CRIADO
# exemplo: sh -c 'emulator @nexus_5_5.1.1 -netspeed lte -memory 512'
START_EMU = "sh -c 'emulator @nexus_5_5.1.1 -gpu off -no-boot-anim -accel auto -netspeed %s -memory %s'"

# Adiciona o IP do container no arquivo config.properties, substituindo o IP padrao
MPOS_IP_CHANGE = 'cd /home/ ; sed -i "s/CHANGE/%s/" config.properties'

# Adiciona um campo padrao no local do IP no arquivo config.properties,
# substituindo o IP corrente pelo valor 'CHANGE' para facilitar a mudanca na proxima execucao
# Exemplo: sed -i "s/172.18.0.2/CHANGE/" config.properties
MPOS_DEFAULT = 'cd /home/ ; sed -i "s/%s/CHANGE/ config.properties"'

# Inicia o servidor MpOS
START_MPOS = "cd /home/ ; java -jar mposplatform.jar"

###################################


##### OUTROS COMANDOS #####
# Retorna o numero de linhas de um arquivo
# Exemplo: wc -l diretorio/android-2-1-lte | cut -f1 -d' '
COUNT_LINES = "wc -l %s/%s | cut -f1 -d' '"
