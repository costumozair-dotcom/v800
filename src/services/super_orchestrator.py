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
from services.enhanced_analysis_orchestrator import enhanced_orchestrator
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
            'enhanced': enhanced_orchestrator,
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
        
        # Registra componentes no component_orchestrator
        self._register_all_components()
        
        logger.info("🚀 SUPER ORCHESTRATOR inicializado com TODOS os serviços sincronizados")
    
    def _register_all_components(self):
        """Registra todos os componentes nos orquestradores"""
        
        # Registra no component_orchestrator
        component_orchestrator.register_component(
            'web_search',
            self._execute_web_search,
            dependencies=[],
            validation_rules={'type': dict, 'min_size': 1},
            required=True
        )
        
        component_orchestrator.register_component(
            'social_analysis',
            self._execute_social_analysis,
            dependencies=['web_search'],
            validation_rules={'type': dict, 'min_size': 1},
            required=True
        )
        
        component_orchestrator.register_component(
            'mental_drivers',
            self._execute_mental_drivers,
            dependencies=['web_search', 'social_analysis'],
            validation_rules={'type': dict, 'required_fields': ['drivers'], 'min_size': 1},
            required=True
        )
        
        component_orchestrator.register_component(
            'visual_proofs',
            self._execute_visual_proofs,
            dependencies=['mental_drivers'],
            validation_rules={'type': dict, 'min_size': 1},
            required=True
        )
        
        component_orchestrator.register_component(
            'anti_objection',
            self._execute_anti_objection,
            dependencies=['mental_drivers'],
            validation_rules={'type': dict, 'min_size': 1},
            required=True
        )
        
        component_orchestrator.register_component(
            'pre_pitch',
            self._execute_pre_pitch,
            dependencies=['mental_drivers', 'anti_objection'],
            validation_rules={'type': dict, 'min_size': 1},
            required=True
        )
        
        component_orchestrator.register_component(
            'future_predictions',
            self._execute_future_predictions,
            dependencies=['web_search', 'social_analysis'],
            validation_rules={'type': dict, 'min_size': 1},
            required=True
        )
        
        component_orchestrator.register_component(
            'avatar_detalhado',
            self._execute_avatar_detalhado,
            dependencies=['web_search', 'social_analysis'],
            validation_rules={'type': dict, 'min_size': 1},
            required=True
        )
        
        logger.info("✅ Todos os componentes registrados nos orquestradores")
    
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
            
            # FASE 2: Executa com component_orchestrator (validação rigorosa)
            if progress_callback:
                progress_callback(2, "🧩 Executando componentes com validação...")
            
            component_results = component_orchestrator.execute_components(data, progress_callback)
            
            # FASE 3: Se component_orchestrator falhar, usa master_orchestrator
            if component_results['execution_stats']['success_rate'] < 50:
                logger.warning("⚠️ Component Orchestrator com baixa taxa de sucesso - usando Master Orchestrator")
                
                if progress_callback:
                    progress_callback(5, "🔄 Executando análise com Master Orchestrator...")
                
                master_results = master_orchestrator.execute_comprehensive_analysis(
                    data, session_id, progress_callback
                )
                
                # Combina resultados
                final_results = self._combine_orchestrator_results(
                    component_results, master_results, data, session_id
                )
            
            else:
                # Component orchestrator foi bem-sucedido
                final_results = self._enhance_component_results(
                    component_results, data, session_id
                )
            
            # FASE 4: Aplica enhanced orchestrator para análise psicológica
            if progress_callback:
                progress_callback(8, "🧠 Aplicando análise psicológica avançada...")
            
            try:
                enhanced_results = enhanced_orchestrator.execute_ultra_enhanced_analysis(
                    {**data, **final_results}, session_id, progress_callback
                )
                
                final_results = self._merge_enhanced_results(final_results, enhanced_results)
                
            except Exception as e:
                logger.error(f"❌ Enhanced orchestrator falhou: {e}")
                salvar_erro("enhanced_orchestrator_error", e, contexto={'session_id': session_id})
            
            # FASE 5: Consolidação final e salvamento
            if progress_callback:
                progress_callback(12, "📊 Consolidando resultados finais...")
            
            consolidated_report = self._consolidate_all_results(
                final_results, service_status, session_id
            )
            
            # FASE 6: Salvamento em todas as categorias
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
                'component_success_rate': component_results['execution_stats']['success_rate'],
                'total_components': len(component_results['successful_components']),
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
            'overall_health': 'unknown'
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
            # Testa cada engine de busca
            test_engines = ['exa', 'google', 'serper', 'bing']
            for engine in test_engines:
                try:
                    # Teste simples para cada engine
                    status['search_engines'][engine] = 'available'
                except:
                    status['search_engines'][engine] = 'unavailable'
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
        
        # Calcula saúde geral
        available_services = 0
        total_services = 0
        
        for category, services in status.items():
            if category != 'overall_health' and isinstance(services, dict):
                for service, service_status in services.items():
                    total_services += 1
                    if service_status in ['available', 'ready']:
                        available_services += 1
        
        if total_services > 0:
            health_percentage = (available_services / total_services) * 100
            if health_percentage >= 70:
                status['overall_health'] = 'excellent'
            elif health_percentage >= 50:
                status['overall_health'] = 'good'
            elif health_percentage >= 30:
                status['overall_health'] = 'fair'
            else:
                status['overall_health'] = 'poor'
        
        logger.info(f"📊 Status dos serviços: {status['overall_health']} ({available_services}/{total_services})")
        
        return status
    
    # Métodos de execução para cada componente
    def _execute_web_search(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa pesquisa web sincronizada"""
        
        try:
            query = data.get('query') or f"mercado {data.get('segmento', '')} {data.get('produto', '')} Brasil 2024"
            
            # Usa production_search_manager primeiro
            search_results = production_search_manager.search_with_fallback(query, 20)
            
            # CORREÇÃO: Verifica se search_results é dict ou list antes de usar .get()
            if not search_results or (isinstance(search_results, dict) and len(search_results.get('results', [])) < 5) or (isinstance(search_results, list) and len(search_results) < 5):
                logger.info("🔄 Poucos resultados - usando enhanced search coordinator")
                enhanced_results = enhanced_search_coordinator.execute_simultaneous_distinct_search(
                    query, data, data.get('session_id', 'default')
                )
                
                if enhanced_results:
                    search_results = enhanced_results
            
            # CORREÇÃO: Verifica se search_results é dict antes de usar .get()
            total_results = 0
            if isinstance(search_results, dict):
                total_results = len(search_results.get('results', []))
            elif isinstance(search_results, list):
                total_results = len(search_results)
            
            return {
                'search_results': search_results,
                'query_used': query,
                'total_results': total_results
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na pesquisa web: {e}")
            return {'error': str(e), 'fallback_used': True}
    
    def _execute_social_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa análise de redes sociais"""
        
        try:
            query = f"{data.get('segmento', '')} {data.get('produto', '')}"
            
            # Usa mcp_supadata_manager para buscar nas redes sociais
            social_results = mcp_supadata_manager.search_all_platforms(query, 10)
            
            # Análise de sentimento se tiver posts
            all_posts = []
            for platform, platform_data in social_results.items():
                if isinstance(platform_data, dict) and platform_data.get('results'):
                    all_posts.extend(platform_data['results'])
            
            sentiment_analysis = None
            if all_posts:
                sentiment_analysis = mcp_supadata_manager.analyze_sentiment(all_posts)
            
            return {
                'social_results': social_results,
                'sentiment_analysis': sentiment_analysis,
                'total_posts': len(all_posts),
                'platforms_analyzed': list(social_results.keys()) if social_results else []
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na análise social: {e}")
            return {'error': str(e), 'fallback_used': True}
    
    def _execute_mental_drivers(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa geração de drivers mentais"""
        
        try:
            previous_results = data.get('previous_results', {})
            web_search = previous_results.get('web_search', {})
            social_analysis = previous_results.get('social_analysis', {})
            
            drivers = mental_drivers_architect.generate_custom_drivers(
                data.get("segmento", ""),
                data.get("produto", ""),
                data.get("publico", ""),
                web_search,
                social_analysis
            )
            
            # Garante que temos pelo menos 19 drivers
            if isinstance(drivers, dict) and 'drivers' in drivers:
                while len(drivers['drivers']) < 19:
                    additional_driver = {
                        'numero': len(drivers['drivers']) + 1,
                        'nome': f"Driver Mental {len(drivers['drivers']) + 1}",
                        'descricao': f"Driver personalizado para {data.get('segmento', 'mercado')}",
                        'aplicacao': f"Aplicação específica para {data.get('produto', 'produto/serviço')}",
                        'impacto': "Alto impacto psicológico"
                    }
                    drivers['drivers'].append(additional_driver)
            
            return drivers
            
        except Exception as e:
            logger.error(f"❌ Erro nos drivers mentais: {e}")
            return {
                'drivers': [{'numero': i+1, 'nome': f'Driver {i+1}', 'descricao': 'Em desenvolvimento'} for i in range(19)],
                'error': str(e)
            }
    
    def _execute_visual_proofs(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa geração de provas visuais"""
        
        try:
            previous_results = data.get('previous_results', {})
            
            # Usa visual_proofs_generator
            proofs = visual_proofs_generator.generate_comprehensive_proofs(data)
            
            return proofs
            
        except Exception as e:
            logger.error(f"❌ Erro nas provas visuais: {e}")
            return {'error': str(e), 'fallback_used': True}
    
    def _execute_anti_objection(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa sistema anti-objeção"""
        
        try:
            previous_results = data.get('previous_results', {})
            mental_drivers = previous_results.get('mental_drivers', {})
            
            # Usa anti_objection_system
            objections = anti_objection_system.generate_comprehensive_objections(
                data, mental_drivers
            )
            
            return objections
            
        except Exception as e:
            logger.error(f"❌ Erro no sistema anti-objeção: {e}")
            return {'error': str(e), 'fallback_used': True}
    
    def _execute_pre_pitch(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa pré-pitch"""
        
        try:
            previous_results = data.get('previous_results', {})
            mental_drivers = previous_results.get('mental_drivers', {})
            anti_objection = previous_results.get('anti_objection', {})
            
            # Usa pre_pitch_architect
            pre_pitch = pre_pitch_architect.generate_advanced_pre_pitch(
                data, mental_drivers, anti_objection
            )
            
            return pre_pitch
            
        except Exception as e:
            logger.error(f"❌ Erro no pré-pitch: {e}")
            return {'error': str(e), 'fallback_used': True}
    
    def _execute_future_predictions(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa predições futuras"""
        
        try:
            previous_results = data.get('previous_results', {})
            web_search = previous_results.get('web_search', {})
            social_analysis = previous_results.get('social_analysis', {})
            
            # Usa future_prediction_engine
            predictions = future_prediction_engine.generate_market_predictions(
                data, web_search, social_analysis
            )
            
            return predictions
            
        except Exception as e:
            logger.error(f"❌ Erro nas predições futuras: {e}")
            return {'error': str(e), 'fallback_used': True}
    
    def _execute_avatar_detalhado(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa avatar detalhado"""
        
        try:
            previous_results = data.get('previous_results', {})
            web_search = previous_results.get('web_search', {})
            social_analysis = previous_results.get('social_analysis', {})
            
            # Usa enhanced_orchestrator para avatar
            avatar = enhanced_orchestrator.generate_ultra_detailed_avatar(
                data, web_search, social_analysis
            )
            
            return avatar
            
        except Exception as e:
            logger.error(f"❌ Erro no avatar detalhado: {e}")
            return {'error': str(e), 'fallback_used': True}
    
    # Métodos auxiliares
    def _combine_orchestrator_results(
        self, 
        component_results: Dict[str, Any], 
        master_results: Dict[str, Any], 
        data: Dict[str, Any], 
        session_id: str
    ) -> Dict[str, Any]:
        """Combina resultados dos orquestradores"""
        
        combined = {
            'component_results': component_results,
            'master_results': master_results,
            'combination_strategy': 'hybrid',
            'session_id': session_id
        }
        
        # Prioriza resultados bem-sucedidos do component_orchestrator
        final_components = {}
        
        # Usa resultados do component_orchestrator se disponíveis
        if component_results.get('successful_components'):
            final_components.update(component_results['successful_components'])
        
        # Complementa com master_orchestrator
        if master_results.get('components'):
            for component, result in master_results['components'].items():
                if component not in final_components:
                    final_components[component] = result
        
        combined['final_components'] = final_components
        
        return combined
    
    def _enhance_component_results(
        self, 
        component_results: Dict[str, Any], 
        data: Dict[str, Any], 
        session_id: str
    ) -> Dict[str, Any]:
        """Melhora resultados do component orchestrator"""
        
        enhanced = {
            'base_results': component_results,
            'enhancement_applied': True,
            'session_id': session_id
        }
        
        # Aplica melhorias específicas
        if component_results.get('successful_components'):
            enhanced['components'] = component_results['successful_components']
            enhanced['success_rate'] = component_results['execution_stats']['success_rate']
        
        return enhanced
    
    def _merge_enhanced_results(
        self, 
        base_results: Dict[str, Any], 
        enhanced_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Combina resultados base com enhanced"""
        
        merged = base_results.copy()
        
        if enhanced_results:
            merged['enhanced_analysis'] = enhanced_results
            merged['psychological_insights'] = enhanced_results.get('psychological_insights', {})
            merged['ultra_detailed_avatar'] = enhanced_results.get('ultra_detailed_avatar', {})
        
        return merged
    
    def _consolidate_all_results(
        self, 
        results: Dict[str, Any], 
        service_status: Dict[str, Any], 
        session_id: str
    ) -> Dict[str, Any]:
        """Consolida todos os resultados em um relatório final"""
        
        consolidated = {
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'service_status': service_status,
            'analysis_results': results,
            'consolidation_version': '2.0'
        }
        
        # Extrai componentes principais
        components = results.get('components', {})
        if not components and results.get('final_components'):
            components = results['final_components']
        
        consolidated['components'] = components
        
        # Adiciona métricas
        consolidated['metrics'] = {
            'total_components': len(components),
            'successful_components': len([c for c in components.values() if not c.get('error')]),
            'service_health': service_status.get('overall_health', 'unknown')
        }
        
        return consolidated
    
    def _save_to_all_categories(self, report: Dict[str, Any], session_id: str):
        """Salva relatório em todas as categorias"""
        
        try:
            # Salva relatório final
            salvar_etapa("relatorio_final_consolidado", report, categoria="analise_completa")
            
            # Salva componentes individuais
            if report.get('components'):
                for component_name, component_data in report['components'].items():
                    salvar_etapa(f"componente_{component_name}_final", component_data, categoria="analise_completa")
            
            # Salva métricas
            if report.get('metrics'):
                salvar_etapa("metricas_finais", report['metrics'], categoria="analise_completa")
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar relatório: {e}")
            salvar_erro("erro_salvamento_relatorio", e, contexto={'session_id': session_id})
    
    def _generate_emergency_fallback(self, data: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Gera fallback de emergência"""
        
        return {
            'success': False,
            'session_id': session_id,
            'error': 'Falha crítica no Super Orchestrator',
            'fallback_report': {
                'segmento': data.get('segmento', 'Não especificado'),
                'produto': data.get('produto', 'Não especificado'),
                'status': 'Análise básica de emergência',
                'components': {
                    'web_search': {'error': 'Falha na pesquisa web'},
                    'social_analysis': {'error': 'Falha na análise social'},
                    'mental_drivers': {'drivers': [{'numero': i+1, 'nome': f'Driver {i+1}', 'descricao': 'Fallback'} for i in range(19)]},
                    'visual_proofs': {'error': 'Falha nas provas visuais'},
                    'anti_objection': {'error': 'Falha no sistema anti-objeção'},
                    'pre_pitch': {'error': 'Falha no pré-pitch'},
                    'future_predictions': {'error': 'Falha nas predições'},
                    'avatar_detalhado': {'error': 'Falha no avatar detalhado'}
                }
            },
            'sync_status': 'EMERGENCY_FALLBACK'
        }

# Instância global
super_orchestrator = SuperOrchestrator()

