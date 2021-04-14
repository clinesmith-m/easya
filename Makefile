INSTALL_DIR=${HOME}/bin

install: ${INSTALL_DIR}/easyA-init ${INSTALL_DIR}/easyZip ${INSTALL_DIR}/easyA

${INSTALL_DIR}/easyA-init: ${INSTALL_DIR}
	cp bin/easyA-init ${INSTALL_DIR}/easyA-init

${INSTALL_DIR}/easyZip: ${INSTALL_DIR}
	cp bin/easyZip ${INSTALL_DIR}/easyZip

${INSTALL_DIR}/easyA: ${INSTALL_DIR}
	ln -s ${PWD}/easyA.py ${INSTALL_DIR}/easyA

${INSTALL_DIR}:
	mkdir ${INSTALL_DIR}
