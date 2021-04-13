INSTALL_DIR=${HOME}/bin

install: ${INSTALL_DIR}/easyA-init ${INSTALL_DIR}/easyZip

${INSTALL_DIR}/easyA-init: ${INSTALL_DIR}
	cp bin/easyA-init ${INSTALL_DIR}/easyA-init

${INSTALL_DIR}/easyZip:
	cp bin/easyZip ${INSTALL_DIR}/easyZip

${INSTALL_DIR}:
	mkdir ${INSTALL_DIR}
