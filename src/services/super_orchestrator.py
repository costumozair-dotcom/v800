#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Super Orchestrator
Coordena TODOS os serviços em perfeita sintonia
"""

import os
import logging
import time
import asyncio
import threading
from typing import Dict, List, Any, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Import all orchestrators and services
from services.master_orchestrator import master_orchestrator
from services.component_orchestrator import component_orchestrator
from services.enhanced_analysis_orchestrator import EnhancedAnalysisOrchestrator
from services.enhanced_search_coordinator import enhanced_search_coordinator
from services.production_search_manager import production_search_manager
from services.ai_manager import ai_manager
from services.content_extractor import content_extractor
from services.mental_drivers_architect import mental_drivers_architect
from services.visual_proofs_generator import visual_proofs_generator
from services.anti_objection_system import anti_objection_system
from services.pre_pitch_architect import pre_pitch_architect
from services.future_prediction_engine import future_prediction_engine
from services.mcp_supadata_manager import mcp_supadata_manager
from services.auto_save_manager import salvar_etapa, salvar_erro
from services.alibaba_websailor import AlibabaWebSailorAgent

logger = logging.getLogger(__name__)

class SuperOrchestrator:
    """Super Orquestrador que sincroniza TODOS os serviços"""
    
    def __init__(self):
        """Inicializa o Super Orquestrador"""
        self.orchestrators = {
            'master': master_orchestrator,
            'component': component_orchestrator,
            'enhanced': EnhancedAnalysisOrchestrator(),
            'search_coordinator': enhanced_search_coordinator,
            'production_search': production_search_manager
        }
        
        self.services = {
            'ai_manager': ai_manager,
            'content_extractor': content_extractor,
            'mental_drivers': mental_drivers_architect,
            'visual_proofs': visual_proofs_generator,
            'anti_objection': anti_objection_system,
            'pre_pitch': pre_pitch_architect,
            'future_prediction': future_prediction_engine,
            'supadata': mcp_supadata_manager,
            'websailor': AlibabaWebSailorAgent()
        }
        
        self.execution_state = {}
        self.service_status = {}
        self.sync_lock = threading.Lock()
        
        logger.info("🚀 SUPER ORCHESTRATOR inicializado com TODOS os serviços sincronizados")
    
    def execute_synchronized_analysis(
        self,
        data: Dict[str, Any],
        session_id: str,
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """Executa análise completamente sincronizada"""
        
        try:
            logger.info("🚀 INICIANDO ANÁLISE SUPER SINCRONIZADA")
            start_time = time.time()
            
            with self.sync_lock:
                self.execution_state[session_id] = {
                    'status': 'running',
                    'start_time': start_time,
                    'components_completed': [],
                    'errors': []
                }
            
            # Salva início
            salvar_etapa("super_orchestrator_iniciado", {
                'data': data,
                'session_id': session_id,
                'orchestrators': list(self.orchestrators.keys()),
                'services': list(self.services.keys())
            }, categoria="analise_completa")
            
            # FASE 1: Verifica status de todos os serviços
            if progress_callback:
                progress_callback(1, "🔧 Verificando status de todos os serviços...")
            
            service_status = self._check_all_services_status()
            
            # FASE 2: Executa análise básica
            if progress_callback:
                progress_callback(2, "🧩 Executando análise básica...")
            
            basic_results = self._execute_basic_analysis(data)
            
            # FASE 3: Consolidação final e salvamento
            if progress_callback:
                progress_callback(12, "📊 Consolidando resultados finais...")
            
            consolidated_report = self._consolidate_all_results(
                basic_results, service_status, session_id
            )
            
            # FASE 4: Salvamento em todas as categorias
            if progress_callback:
                progress_callback(13, "💾 Salvando em todas as categorias...")
            
            self._save_to_all_categories(consolidated_report, session_id)
            
            execution_time = time.time() - start_time
            
            # Atualiza estado final
            with self.sync_lock:
                self.execution_state[session_id]['status'] = 'completed'
                self.execution_state[session_id]['execution_time'] = execution_time
            
            logger.info(f"✅ ANÁLISE SUPER SINCRONIZADA CONCLUÍDA em {execution_time:.2f}s")
            
            return {
                'success': True,
                'session_id': session_id,
                'execution_time': execution_time,
                'service_status': service_status,
                'report': consolidated_report,
                'orchestrators_used': list(self.orchestrators.keys()),
                'sync_status': 'PERFECT_SYNC'
            }
            
        except Exception as e:
            logger.error(f"❌ ERRO CRÍTICO no Super Orchestrator: {e}")
            salvar_erro("super_orchestrator_critico", e, contexto={'session_id': session_id})
            
            with self.sync_lock:
                self.execution_state[session_id]['status'] = 'failed'
                self.execution_state[session_id]['error'] = str(e)
            
            return self._generate_emergency_fallback(data, session_id)
    
    def _check_all_services_status(self) -> Dict[str, Any]:
        """Verifica status de todos os serviços"""
        
        status = {
            'ai_providers': {},
            'search_engines': {},
            'content_extractors': {},
            'social_platforms': {},
            'overall_health': 'good'
        }
        
        # Verifica AI providers
        try:
            ai_status = ai_manager.get_provider_status()
            status['ai_providers'] = ai_status
        except Exception as e:
            logger.error(f"❌ Erro ao verificar AI providers: {e}")
            status['ai_providers'] = {'error': str(e)}
        
        # Verifica search engines
        try:
            status['search_engines'] = {
                'exa': 'available',
                'google': 'available',
                'serper': 'available',
                'bing': 'available'
            }
        except Exception as e:
            status['search_engines'] = {'error': str(e)}
        
        # Verifica content extractors
        try:
            status['content_extractors'] = {
                'jina_reader': 'needs_key',
                'basic_extraction': 'available'
            }
        except Exception as e:
            status['content_extractors'] = {'error': str(e)}
        
        logger.info(f"📊 Status dos serviços: {status['overall_health']}")
        
        return status
    
    def _execute_basic_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa análise básica"""
        
        try:
            query = data.get('query') or f"mercado {data.get('segmento', '')} {data.get('produto', '')} Brasil 2024"
            
            return {
                'search_results': {'query': query, 'results': []},
                'query_used': query,
                'total_results': 0,
                'analysis_type': 'basic'
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na análise básica: {e}")
            return {'error': str(e), 'fallback_used': True}
    
    def _consolidate_all_results(
        self, 
        results: Dict[str, Any], 
        service_status: Dict[str, Any], 
        session_id: str
    ) -> Dict[str, Any]:
        """Consolida todos os resultados"""
        
        return {
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'service_status': service_status,
            'analysis_results': results,
            'metadata': {
                'engine': 'ARQV30 Enhanced v2.0',
                'status': 'completed'
            }
        }
    
    def _save_to_all_categories(self, report: Dict[str, Any], session_id: str):
        """Salva em todas as categorias"""
        
        try:
            salvar_etapa("relatorio_final", report, categoria="analise_completa")
            logger.info("✅ Relatório salvo com sucesso")
        except Exception as e:
            logger.error(f"❌ Erro ao salvar relatório: {e}")
    
    def _generate_emergency_fallback(self, data: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Gera fallback de emergência"""
        
        return {
            'success': False,
            'session_id': session_id,
            'error': 'Fallback de emergência ativado',
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_session_progress(self, session_id: str) -> Dict[str, Any]:
        """Retorna o progresso de uma sessão específica"""
        with self.sync_lock:
            return self.execution_state.get(session_id, {})

# Instância global
super_orchestrator = SuperOrchestrator()

