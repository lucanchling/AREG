#-----------------------------------------------------------------------------
set(MODULE_NAME PRE_ASO_IOS)



set(MODULE_PYTHON_SCRIPTS 
  ${MODULE_NAME}.py)

SlicerMacroBuildScriptedCLI(
  NAME ${MODULE_NAME}
  RESOURCES ${MODULE_PYTHON_SCRIPTS}
  
  )